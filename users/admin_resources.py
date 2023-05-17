from import_export import resources

from users.models import Student, Employee, Direction, BankAccount, CustomUser


class StudentResource(resources.ModelResource):
	class Meta:
		model = Student


class EmployeeResource(resources.ModelResource):
	class Meta:
		model = Employee


class DirectionResource(resources.ModelResource):
	class Meta:
		model = Direction


class BankAccountResource(resources.ModelResource):
	class Meta:
		model = BankAccount


class CustomBaseUserResource(resources.ModelResource):
	class Meta:
		model = CustomUser
