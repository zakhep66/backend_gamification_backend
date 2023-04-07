from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем
        """
        if not email:
            raise ValueError('Не указан Email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class StudentManager(CustomUserManager):
    def create_superuser(self, email, password, **extra_fields):
        pass


class EmployeeManager(CustomUserManager):
    def create_superuser(self, email, password, **extra_fields):
        pass
