from django.contrib import admin
from .models import Student, Employee, Direction, BankAccount


class StudentAdmin(admin.ModelAdmin):
    """Конфигурация модели студента в админке"""

    def save_model(self, request, obj, form, change):
        if not change or not obj.password or obj.password is not None and not obj.has_usable_password():
            obj.set_password(form.cleaned_data['password'])
        obj.save()


class EmployeeAdmin(admin.ModelAdmin):
    """Конфигурация модели сотрудника в админке"""

    def save_model(self, request, obj, form, change):
        if not change or not obj.password or obj.password is not None and not obj.has_usable_password():
            obj.set_password(form.cleaned_data['password'])
        obj.save()


admin.site.register(Student, StudentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Direction)
admin.site.register(BankAccount)
