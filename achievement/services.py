from rest_framework import status

from achievement.models import Achievement
from achievement.serializers import AchievementSerializer


class AchievementHandler:
    @staticmethod
    def get_student_achievement(student_id):
        student_achievement = Achievement.objects.filter(students__id=student_id)
        serializer_data = AchievementSerializer(student_achievement, many=True).data
        return serializer_data, status.HTTP_200_OK
