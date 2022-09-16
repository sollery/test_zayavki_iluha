from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subdivision, Position


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = []

    model = CustomUser
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ['email', 'fio', 'subdivision','position']

    # Add user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'email',
                    'fio',
                    'subdivision',
                    'position',
                )
            }
        )
    )
    # Edit user
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'fio',
                    'subdivision',
                    'position',
                )
            }
        )
    )


@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Position)
class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ['title']
