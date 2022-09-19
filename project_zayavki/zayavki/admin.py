from django.contrib import admin
from .models import Employee, Facility, ApplicationTest, EmployeeInSubdivision, ListApplication


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['title','subdivision']


@admin.register(EmployeeInSubdivision)
class EmployeeInSubdivisionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'subdivision']

@admin.register(ApplicationTest)
class ApplicationTestAdmin(admin.ModelAdmin):
    list_display = ['customer','date_application','facility','employee','employee_count','subdivision','created','is_active','comment','status','application_id']


@admin.register(ListApplication)
class ListApplicationAdmin(admin.ModelAdmin):
    list_display = ['customer','date_applications','subdivision','status','created']

# Register your models here.
