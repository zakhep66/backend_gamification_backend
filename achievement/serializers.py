from rest_framework import serializers

from achievement.models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
