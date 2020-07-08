
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

# Создаём подклассы форм UserCreationForm и UserChangeForm, чтобы они использовали новую модель CustomUser:

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('login',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('login',)
