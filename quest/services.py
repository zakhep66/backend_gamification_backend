from django.db import transaction
from rest_framework import status

from quest.models import Quest
from transfer.services import TransactionHandler
from users.models import Student

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
