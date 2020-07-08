
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Создаём класс для админки:
class CustomUserAdmin(UserAdmin):

    # Указываем django использовать формы (из forms.py):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('login',)
    list_filter = ('login',)
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2',)}
        ),
    )
    search_fields = ('login',)
    ordering = ('login',)

# регистрируем класс в админке:
admin.site.register(CustomUser, CustomUserAdmin)
