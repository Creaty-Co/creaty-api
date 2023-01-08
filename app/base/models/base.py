from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        clean=True,
        clean_exclude=None,
    ):
        if clean:
            self.full_clean(exclude=clean_exclude)
        models.Model.save(self, force_insert, force_update, using, update_fields)
