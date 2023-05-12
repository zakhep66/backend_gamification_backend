from django.db import models

import utils


class Achievement(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to=utils.get_upload_path_for_achievement)
	sum_reward = models.PositiveIntegerField()
	description = models.TextField()
	date_time = models.DateTimeField(auto_now_add=True)
	achievement_type = models.ForeignKey('AchievementType', on_delete=models.CASCADE, related_name='achievement')

	class Meta:
		verbose_name = 'Ачивка'
		verbose_name_plural = 'Ачивки'

	def __str__(self):
		return self.name


class AchievementType(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Тип ачивки'
		verbose_name_plural = 'Типы ачивок'
