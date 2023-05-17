from django.db import transaction
from rest_framework import status

from quest.models import Quest
from quest.serializers import QuestSerializer
from transfer.services import TransactionHandler

from rest_framework.exceptions import ValidationError


class QuestHandler:
    @staticmethod
    @transaction.atomic()
    def quest_completed(quest: Quest):
        try:
            TransactionHandler.quest_transaction(student_id=quest.student_id, award_sum=quest.sum)
        except Exception as e:
            error_message = str(e)
            raise ValidationError(error_message)

        return {'detail': 'Награда зачислена'}, status.HTTP_200_OK

    @staticmethod
    def get_all_is_active():
        quests = Quest.objects.filter(is_active=True)
        serializer = QuestSerializer(quests, many=True)
        return serializer.data, status.HTTP_200_OK

    @staticmethod
    def get_student_quest(student_id: int):
        qs = Quest.objects.filter(student_id=student_id)
        serializer = QuestSerializer(qs, many=True)
        return serializer.data, status.HTTP_200_OK

    @staticmethod
    def get_employee_quest(employee_id: int):
        qs = Quest.objects.filter(employee_id=employee_id)
        serializer = QuestSerializer(qs, many=True)
        return serializer.data, status.HTTP_200_OK
