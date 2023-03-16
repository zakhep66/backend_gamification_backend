from django.db import models

from user.models import User


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


class Direction(models.Model):
	student_id = models.ManyToManyField('Student')
	name = models.CharField(max_length=50, blank=False, null=False)
	icon = models.ImageField(upload_to=...)  # todo написать бла бла бла

	class Meta:
		verbose_name = 'Направление'
		verbose_name_plural = 'Направления'
