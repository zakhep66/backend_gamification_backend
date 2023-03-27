from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """Переопределил метод сохранения модели, чтобы при создании или
        изменении модели не через API пароль хешировался
        """

        # Проверяем, есть ли уже запись в базе данных для этого объекта
        if self.pk:
            # Если пароль был изменен, то хешируем его заново
            old_student = CustomUser.objects.get(pk=self.pk)
            if self.password != old_student.password:
                self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Employee(CustomUser):
    EMPLOYEE_ROLE = (
        ('main_admin', 'Главный администратор'),  # Тимур
        ('manager', 'Админ'),
        ('coach', 'Коуч'),
        ('curator', 'Куратор')
    )

    # user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    employee_role = models.CharField(max_length=50, choices=EMPLOYEE_ROLE, null=False, blank=False)
    # education_direction = models.ForeignKey('EducationDirection', on_delete=models.CASCADE, blank=True, null=True)
    one_fact = models.CharField(max_length=100, blank=True, null=True)
    two_fact = models.CharField(max_length=100, blank=True, null=True)
    false_fact = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Student(CustomUser):
    STUDENT_STATUS = (
        ('active', 'Активный'),
        ('not_active', 'Неактивный'),
        ('block', 'Заблокирован'),
    )

    # user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    in_lite = models.BooleanField(blank=False, null=False)
    # bank_account_id = models.OneToOneField('BankAccount', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STUDENT_STATUS, blank=False, null=False, default='active')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
