from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomAdminPasswordChangeForm
from .models import Student, Employee, Direction, BankAccount, StudentProfile


class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name')}),
		(_('Permissions'), {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		(_('Important dates'), {'fields': ('last_login',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)
	readonly_fields = ('password_placeholder',)
	list_display = ('email', 'first_name', 'last_name', 'is_staff')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)

	def password_placeholder(self, instance):
		return _("******")

	password_placeholder.short_description = _("Password")


class StudentAdmin(CustomUserAdmin):
	change_password_form = CustomAdminPasswordChangeForm

	def save_model(self, request, obj, form, change):
		if change and form.cleaned_data["password"]:
			obj.password = make_password(form.cleaned_data["password"])
		super().save_model(request, obj, form, change)


class EmployeeAdmin(CustomUserAdmin):
	change_password_form = CustomAdminPasswordChangeForm

	def save_model(self, request, obj, form, change):
		if change and form.cleaned_data["password"]:
			obj.password = make_password(form.cleaned_data["password"])
		super().save_model(request, obj, form, change)


admin.site.register(Student, StudentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Direction)
admin.site.register(BankAccount)
admin.site.register(StudentProfile)
