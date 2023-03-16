from django.db import models


class Direction(models.Model):
	student_id = models.ManyToManyField('Student')
	name = models.CharField(max_length=50, blank=False, null=False)
	icon = models.ImageField(upload_to=...)  # todo написать бла бла бла

	class Meta:
		verbose_name = 'Направление'
		verbose_name_plural = 'Направления'

class 
