from django.contrib import admin

from quest.models import Quest, QuestType


admin.site.register(Quest)
admin.site.register(QuestType)
