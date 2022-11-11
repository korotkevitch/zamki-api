from django.db import models
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
import uuid
import os


def service_image_file_path(instance, filename):
    """Generate file path for new image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'service', filename)


class Service(models.Model):
    service = models.CharField('Название услуги', max_length=20, blank=True)
    image = models.ImageField('Фото', null=True, upload_to=service_image_file_path)
    description = models.CharField('Описание', max_length=2000, blank=True)

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="%s" style="width:100px; height:80px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_preview.short_description = 'Фото'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Список услуг'

    def __str__(self):
        return self.service
