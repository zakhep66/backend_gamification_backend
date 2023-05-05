from import_export import resources

from users.models import Student, Employee


class StudentResource(resources.ModelResource):
	class Meta:
		model = Student


class EmployeeResource(resources.ModelResource):
	class Meta:
		model = Employee
