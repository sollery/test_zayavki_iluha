from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import CustomUser, Subdivision
from django.utils import timezone


class Employee(models.Model):
    title = models.CharField('Работник', max_length=50, default='')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='subdivisionemp', null=True)

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


class EmployeeInSubdivision(models.Model):
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='Subdivisions',)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='Employees')

    def __str__(self):
        return "{}({})".format(self.employee.title,self.subdivision.title)

    class Meta:
        verbose_name = 'Работник на подразделении'
        verbose_name_plural = 'Работники на подразделении'
        unique_together = ('subdivision', 'employee',)

# Create your models here.


class ListApplication(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='customer_applicationsList', null=True)
    created = models.DateTimeField(default=timezone.now)
    date_applications = models.DateField('Дата исполнения')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, related_name='subdivisioninApplicationlist',
                                    null=True)
    status = models.CharField('Статус', max_length=30,default='на рассмотрении')
    viza = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='viza_application', null=True,default=None,blank=True)
    comment = models.TextField('Комментарий', max_length=300, default='Нет комментария')

    def __str__(self):
        return "заказчик: {} подразделение: {} дата заказа услуг: {} дата создания заявки: {}"\
            .format(self.customer.fio, self.subdivision.title, self.date_applications,self.created)

    class Meta:
        verbose_name = 'Список заявок'
        verbose_name_plural = 'Список заявок'

    def check_status(self):
        if self.status == 'на рассмотрении':
            return False
        else:
            return True

    def color_status(self):
        if self.status == "Согласованно":
            return "success"
        elif self.status == "Не согласованно":
            return "danger"


    def change_zayavki(self):
        if self.status == 'на рассмотрении' or self.status == 'Не согласованно':
            return True
        return False


class ApplicationTest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='customer_application',null=True)
    date_application = models.DateField('Дата заявки')
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, related_name='facilityinapplication',null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='employeeinapplication',null=True)
    employee_count = models.PositiveIntegerField('Количество работников')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, related_name='subdivisioninapplication',
                                    null=True)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=30,default='на рассмотрении')
    application_id = models.ForeignKey(ListApplication, on_delete=models.CASCADE, related_name='subdivisioninapplication',)



    def __str__(self):
        return "заказчик: {} объект: {} дата заказа услуг: {} дата создания заявки: {}"\
            .format(self.customer.fio,self.facility,self.date_application,self.created)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


