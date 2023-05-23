from django.db import models

from users.models import Employee, Student


class Quest(models.Model):
	employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
	student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, blank=True, null=True)
	type = models.ForeignKey('QuestType', on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	description = models.TextField()
	sum = models.PositiveIntegerField(default=0)
	date_time = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Квест'
		verbose_name_plural = 'Квесты'


class QuestType(models.Model):
	name = models.CharField(max_length=50)
	color = models.CharField(max_length=20)
	min_sum = models.PositiveIntegerField()
	max_sum = models.PositiveIntegerField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Тип квеста'
		verbose_name_plural = 'Типы квестов'
