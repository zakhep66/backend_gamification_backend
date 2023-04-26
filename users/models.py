from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

import utils
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

    def save(self, *args, **kwargs):
        if self.pk is not None:  # проверяем, что объект уже сохранен в базе данных
            original = type(self).objects.get(pk=self.pk)  # загружаем объект из базы данных
            if original.password != self.password:  # проверяем, изменялся ли пароль
                self.password = make_password(self.password)
        else:
            self.password = make_password(self.password)  # хешируем пароль при создании записи
        super().save(*args, **kwargs)


class AbstractUserModel(models.Model):
    USER_ROLE = (
        ('manager', 'Админ'),
        ('coach', 'Коуч'),
        ('curator', 'Куратор'),
        ('student', 'Студент'),
    )

    user_role = models.CharField(choices=USER_ROLE, max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to=get_upload_path_for_users, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        abstract = True


class Employee(CustomUser, AbstractUserModel):
    direction = models.ForeignKey('Direction', on_delete=models.DO_NOTHING, blank=True, null=True,
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
    bank_account_id = models.OneToOneField('BankAccount', on_delete=models.CASCADE, related_name='student')
    status = models.CharField(max_length=50, choices=STUDENT_STATUS, blank=False, null=False, default='active')
    direction = models.ManyToManyField('Direction', related_name='direction', null=True, blank=True)

    objects = StudentManager()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class BankAccount(models.Model):
    balance = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Активен' if self.is_active else 'Заблокирован'

    class Meta:
        verbose_name = 'Банковский аккаунт'
        verbose_name_plural = 'Банковские аккаунты'


class Direction(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.ImageField(upload_to=utils.get_upload_path_for_icon, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


# class Buy(models.Model):
# 	store_product_id = models.ForeignKey('StoreProduct', on_delete=models.CASCADE)
# 	student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
# 	date_time = models.DateTimeField(auto_now_add=True)
# 	content = models.TextField()
# 	status = models.BooleanField(default=False)
#
# 	class Meta:
# 		verbose_name = 'Покупка'
# 		verbose_name_plural = 'Покупки'
#
# 	def __str__(self):
# 		return self.student_id.first_name + 'купил' + self.store_product_id.name
