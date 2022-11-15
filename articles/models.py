from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from services.models import Service
from django.utils.safestring import mark_safe
import uuid
import os


def article_image_file_path(instance, filename):
    """Generate file path for new image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'article', filename)


class Article(models.Model):
    title = models.CharField("Название", max_length=50)
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Тема/сервис")
    storyline = models.TextField("О чем статья", blank=True)
    text = models.TextField("Текст статьи", blank=True)
    image = models.ImageField('Фото', null=True, upload_to=article_image_file_path)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    active = models.BooleanField("Опубликовано", default=True)
    avg_rating = models.FloatField("Рейтинг", default=0)
    number_rating = models.IntegerField("Количество оценок", default=0)
    created = models.DateTimeField("Написано", auto_now_add=True)
    updated = models.DateTimeField("Отредактировано", auto_now=True, null=True)

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="%s" style="width:100px; height:80px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_preview.short_description = 'Фото'

    def __str__(self):
        return self.title

    class META:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья", related_name="articles")
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    rating = models.PositiveIntegerField("Рейтинг", validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField("Отзыв", max_length=200, null=True)
    active = models.BooleanField(default=True, verbose_name="Опубликовано")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Написано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Исправлено")

    class META:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.rating) + " | " + self.article.title + " | " + str(self.review_user)