from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


admin.site.unregister(User)


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'birth_date', 'gender', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
