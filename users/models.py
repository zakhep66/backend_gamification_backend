from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


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
	first_name = models.CharField(max_length=50, null=False, blank=False)
	last_name = models.CharField(max_length=50, null=False, blank=False)

	class Meta:
		abstract = True


class Employee(CustomUser, AbstractUserModel):
	EMPLOYEE_ROLE = (
		('main_admin', 'Главный администратор'),  # Тимур
		('manager', 'Админ'),
		('coach', 'Коуч'),
		('curator', 'Куратор')
	)

	employee_role = models.CharField(max_length=50, choices=EMPLOYEE_ROLE, null=False, blank=False)
	# education_direction = models.ForeignKey('EducationDirection', on_delete=models.CASCADE, blank=True, null=True)
	first_fact = models.CharField(max_length=100, blank=True, null=True)
	second_fact = models.CharField(max_length=100, blank=True, null=True)
	false_fact = models.CharField(max_length=100, blank=True, null=True)

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
	# bank_account_id = models.OneToOneField('BankAccount', on_delete=models.CASCADE)
	status = models.CharField(max_length=50, choices=STUDENT_STATUS, blank=False, null=False, default='active')

	class Meta:
		verbose_name = 'Студент'
		verbose_name_plural = 'Студенты'
