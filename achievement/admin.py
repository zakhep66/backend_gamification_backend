from django.contrib import admin

from achievement.models import Achievement, AchievementType

admin.site.register(Achievement)
admin.site.register(AchievementType)
