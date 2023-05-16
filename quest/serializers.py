from rest_framework import serializers

from quest.models import Quest, QuestType


class QuestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quest
		fields = '__all__'


class QuestTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestType
		fields = '__all__'
