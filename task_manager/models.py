from django.db import models
from django.contrib.auth import get_user_model

from statuses.models import Status

User = get_user_model()


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author', verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='executor', verbose_name='Исполнитель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    labels = models.ManyToManyField(Label, blank=True, verbose_name='Метки')

    def __str__(self):
        return self.name
