from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']
    
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None,
        clean=True, clean_exclude=None
    ):
        if clean:
            self.full_clean(exclude=clean_exclude)
        super().save(force_insert, force_update, using, update_fields)
