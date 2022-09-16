from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class Subdivision(models.Model):
    title = models.CharField('Подразделение', max_length=50, default='')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Position(models.Model):
    title = models.CharField('Должность', max_length=50, default='')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class CustomUser(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    fio = models.CharField('ФИО', max_length=255, default='')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='user_subdivision', null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='user_position', null=True)

    def __str__(self):
        return self.fio
# Create your models here.



