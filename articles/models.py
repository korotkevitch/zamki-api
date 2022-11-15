from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from services.models import Service


class Article(models.Model):
    title = models.CharField("Название", max_length=50)
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Тема/сервис")
    storyline = models.TextField("О чем статья", blank=True)
    text = models.TextField("Текст статьи", blank=True)
    active = models.BooleanField("Опубликована", default=True)
    avg_rating = models.FloatField("Рейтинг", default=0)
    number_rating = models.IntegerField("Количество оценок", default=0)
    created = models.DateTimeField("Дата написания", auto_now_add=True)

    def __str__(self):
        return self.title

    class META:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'