from django.contrib import admin
from .models import Employee, Facility, EmployeeInFacility, ApplicationTest


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['title','subdivision']


@admin.register(EmployeeInFacility)
class EmployeeInFacilityAdmin(admin.ModelAdmin):
    list_display = ['employee', 'facility']

@admin.register(ApplicationTest)
class ApplicationTestAdmin(admin.ModelAdmin):
    list_display = ['customer','data_application','facility','employee','employee_count','subdivision','created','is_active','comment']


# Register your models here.
