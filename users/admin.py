from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from .admin_resources import EmployeeResource, StudentResource, DirectionResource, BankAccountResource
from .forms import CustomAdminPasswordChangeForm
from .models import Student, Employee, Direction, BankAccount, StudentProfile


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', ),
        }),
    )
    readonly_fields = ('password_placeholder',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def password_placeholder(self, instance):
        return _("******")

    password_placeholder.short_description = _("Password")


@admin.register(Student)
class StudentAdmin(CustomUserAdmin, ImportExportModelAdmin):
    change_password_form = CustomAdminPasswordChangeForm
    resource_class = StudentResource

    fieldsets = CustomUserAdmin.fieldsets + (
        (_('Student Information'), {'fields': (
            'telegram', 'about', 'portfolio_link', 'in_lite', 'bank_account_id', 'status', 'direction',
            'student_profile',
            'achievement')}),
    )
    list_display = CustomUserAdmin.list_display + (
        'telegram', 'about', 'portfolio_link', 'in_lite', 'bank_account_id', 'status', 'direction_list',
        'student_profile', 'achievement_list'
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('in_lite', 'bank_account_id', 'student_profile', 'user_role'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if change and form.cleaned_data["password"]:
            obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

    def direction_list(self, obj):
        return ", ".join([direction.name for direction in obj.direction.all()])

    direction_list.short_description = _('Directions')

    def achievement_list(self, obj):
        return ", ".join([achievement.name for achievement in obj.achievement.all()])

    achievement_list.short_description = _('Achievements')


@admin.register(Employee)
class EmployeeAdmin(CustomUserAdmin, ImportExportModelAdmin):
    change_password_form = CustomAdminPasswordChangeForm
    resource_class = EmployeeResource

    fieldsets = CustomUserAdmin.fieldsets + (
        (_('Employee Information'), {'fields': (
            'first_fact', 'second_fact', 'false_fact', 'direction', 'user_role'
        )}),
    )
    list_display = CustomUserAdmin.list_display + (
        'first_fact', 'second_fact', 'false_fact', 'direction',
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('user_role', ),
        }),
    )

    def save_model(self, request, obj, form, change):
        if change and form.cleaned_data["password"]:
            obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


@admin.register(Direction)
class DirectionAdmin(ImportExportModelAdmin):
    resource_class = DirectionResource


@admin.register(BankAccount)
class BankAccountAdmin(ImportExportModelAdmin):
    resource_class = BankAccountResource


admin.site.register(StudentProfile)
