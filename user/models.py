from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from utils import get_upload_path


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
	avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
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
