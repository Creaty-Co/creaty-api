from abc import ABC

import cloudinary
from cloudinary import uploader
from cloudinary_storage.storage import MediaCloudinaryStorage as _MediaCloudinaryStorage
from django.core.files.uploadedfile import UploadedFile


class MediaCloudinaryStorage(_MediaCloudinaryStorage, ABC):
    def _save(self, name, content):
        name = self._normalise_name(name)
        name = self._prepend_prefix(name)
        parts = name.rsplit('-', 1)
        if len(parts) == 2:
            name, version = parts
            content = UploadedFile(content, name)
            response = self._upload(name, content)
            return f"{response['public_id']}-{version}"
        content = UploadedFile(content, name)
        response = self._upload(name, content)
        return response['public_id']

    def delete(self, name):
        response = uploader.destroy(
            name.rsplit('-', 1)[0],
            invalidate=True,
            resource_type=self._get_resource_type(name),
        )
        return response['result'] == 'ok'

    def _get_url(self, name: str) -> str:
        name = self._prepend_prefix(name)
        parts = name.rsplit('-', 1)
        if len(parts) == 2:
            name, version = parts
            cloudinary_resource = cloudinary.CloudinaryResource(
                name,
                default_resource_type=self._get_resource_type(name),
                version=version,
            )
        else:
            cloudinary_resource = cloudinary.CloudinaryResource(
                name, default_resource_type=self._get_resource_type(name)
            )
        return cloudinary_resource.url
