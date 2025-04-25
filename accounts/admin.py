from django.contrib import admin
from .models import Roles, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    filter_horizontal = ('role_permissions',)
    
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'last_login', 'is_staff', 'is_active', 'cargo')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'img_user')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Cargo', {'fields': ('cargo',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'cargo', 'img_user'),
        }),
    )
