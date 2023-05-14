from celery import shared_task

from achievement.models import Achievement, AchievementType
from users.models import Student


class CeleryAchievementTasks:
    @staticmethod
    @shared_task
    def award_achievement_on_first_purchase(student_id):
        student = Student.objects.get(id=student_id)
        achievement_type = AchievementType.objects.get(name='first_buy')
        first_purchase_achievement = Achievement.objects.get(achievement_type=achievement_type)

        # Проверяем, есть ли уже эта ачивка у студента
        if first_purchase_achievement not in student.achievement.all():
            # Добавляем ачивку к студенту
            student.achievement.add(first_purchase_achievement)
            student.save()

    @staticmethod
    @shared_task
    def award_achievement_on_first_change_avatar(student_id):
        student = Student.objects.get(id=student_id)
        achievement_type = AchievementType.objects.get(name='change_avatar')
        first_change_avatar = Achievement.objects.get(achievement_type=achievement_type)

        # Проверяем, если ти такая ачивка
        if first_change_avatar not in student.achievement.all():
            # Добавляем такую ачивку
            student.achievement.add(first_change_avatar)
            student.save()
