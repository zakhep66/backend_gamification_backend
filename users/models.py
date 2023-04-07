from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager, StudentManager, EmployeeManager
from utils import get_upload_path_for_users


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная базовая модель пользователя системы"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AbstractUserModel(models.Model):
    image = models.ImageField(upload_to=get_upload_path_for_users)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        abstract = True


class Employee(CustomUser, AbstractUserModel):
    EMPLOYEE_ROLE = (
        ('manager', 'Админ'),
        ('coach', 'Коуч'),
        ('curator', 'Куратор')
    )
    employee_role = models.CharField(max_length=50, choices=EMPLOYEE_ROLE, null=False, blank=False)
    direction = models.ForeignKey('Direction', on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='Направление')
    first_fact = models.CharField(max_length=100, blank=True, null=True)
    second_fact = models.CharField(max_length=100, blank=True, null=True)
    false_fact = models.CharField(max_length=100, blank=True, null=True)

    objects = EmployeeManager()

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Student(CustomUser, AbstractUserModel):
    STUDENT_STATUS = (
        ('active', 'Активный'),
        ('not_active', 'Неактивный'),
        ('block', 'Заблокирован'),
    )

    telegram = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    in_lite = models.BooleanField(blank=False, null=False)
    bank_account_id = models.OneToOneField('BankAccount', on_delete=models.CASCADE, related_name='Банковский_аккаунт')
    status = models.CharField(max_length=50, choices=STUDENT_STATUS, blank=False, null=False, default='active')
    direction = models.ManyToManyField('Direction', related_name='direction')

    objects = StudentManager()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


#####################################
#####################################
#####################################
class BankAccount(models.Model):
    balance = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Баланс активен' if self.is_active is True else 'Баланс заблокирован'

    class Meta:
        verbose_name = 'Банковский аккаунт'
        verbose_name_plural = 'Банковские аккаунты'


class Direction(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
