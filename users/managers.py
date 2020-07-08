
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, login, email=None, password=None, **extra_fields):
        if not login:
            raise ValueError(_('login is reauiered.'))

        email = self.normalize_email(email)
        # user = self.model(login=login, email=email, **extra_fields)
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, login, email=None, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # return self.create_user(login, password, **extra_fields)
        return self.create_user(login, email=email, password=password, **extra_fields)
