from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SpamNumber

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'phone_number', 'email', 'spam')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Spam', {'fields': ('spam',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'email', 'password1', 'password2', 'spam'),
        }),
    )

class SpamNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'spam_count')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SpamNumber, SpamNumberAdmin)


# Register your models here.
