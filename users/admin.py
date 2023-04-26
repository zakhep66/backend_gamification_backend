from django.contrib import admin
from .models import Student, Employee, Direction, BankAccount


admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Direction)
admin.site.register(BankAccount)
