from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import CustomUser, Subdivision
from django.utils import timezone


class Employee(models.Model):
    title = models.CharField('Работник', max_length=50, default='')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class Facility(models.Model):
    title = models.CharField('Объект', max_length=50, default='')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='subdivisions', null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class EmployeeInFacility(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='facilitys', null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='Employees', null=True)

    def __str__(self):
        return "{} на {}".format(self.employee.title,self.facility.title)

    class Meta:
        verbose_name = 'Работник на объекте'
        verbose_name_plural = 'Работники на объектах'
        unique_together = ('facility', 'employee',)

# Create your models here.


class ApplicationTest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_application')
    data_application = models.DateField('Дата заявки')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='facilityinapplication',)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeeinapplication')
    employee_count = models.PositiveIntegerField('Количество работников',
                                                 validators=[MinValueValidator(1), MaxValueValidator(100)])
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='subdivisioninapplication')
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    comment = models.TextField('Комментарий', blank=True)

    def __str__(self):
        return "заказчик: {} объект: {} дата заказа услуг: {} дата создания заявки: {}"\
            .format(self.customer.fio,self.facility.title,self.data_application,self.created)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'