from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('Email field must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	# todo прописать функцию для генерации имени картинки и пути к ней
	avatar = models.ImageField(upload_to=..., blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True


class Employee(User):
	EMPLOYEE_ROLE = (
		('main_admin', 'Главный администратор'),  # Тимур
		('manager', 'Админ'),
		('coach', 'Коуч'),
		('curator', 'Куратор')
	)

	employee_role = models.CharField(max_length=50, choices=EMPLOYEE_ROLE, null=False, blank=False)
	education_direction = models.ForeignKey('EducationDirection', on_delete=models.CASCADE, blank=True, null=True)
	one_fact = models.CharField(max_length=100, blank=True, null=True)
	two_fact = models.CharField(max_length=100, blank=True, null=True)
	false_fact = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Сотрудник'
		verbose_name_plural = 'Сотрудники'


class Student(User):
	STUDENT_STATUS = (
		('active', 'Активный'),
		('not_active', 'Неактивный'),
		('block', 'Заблокирован'),
	)

	telegram = models.CharField(max_length=100, blank=True, null=True)
	about = models.TextField(blank=True, null=True)
	portfolio_link = models.URLField(blank=True, null=True)
	in_lite = models.BooleanField(blank=False, null=False)
	bank_account_id = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
	status = models.CharField(choices=STUDENT_STATUS, blank=False, null=False, default='active')

	class Meta:
		verbose_name = 'Студент'
		verbose_name_plural = 'Студенты'


class Administrator(User):
	class Meta:
		verbose_name = 'Системный администратор'
		verbose_name_plural = 'Системные администраторы'
