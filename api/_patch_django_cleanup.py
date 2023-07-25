from django_cleanup import cache, handlers
from django_cleanup.handlers import delete_file


def delete_old_post_save(sender, instance, raw, created, update_fields, using, **_):
    if raw:
        return
    if not created:
        for field_name, new_file in cache.fields_for_model_instance(instance):
            if update_fields is None or field_name in update_fields:
                old_file = cache.get_field_attr(instance, field_name)
                if old_file.name is not None and new_file.name is not None:
                    if (
                        old_file.name.rsplit('-', 1)[0]
                        != new_file.name.rsplit('-', 1)[0]
                    ):
                        delete_file(
                            sender, instance, field_name, old_file, using, 'updated'
                        )
    cache.make_cleanup_cache(instance)


handlers.delete_old_post_save = delete_old_post_save
