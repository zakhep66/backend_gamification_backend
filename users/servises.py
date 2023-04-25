from django.db.models import Sum
from rest_framework import status

from users.models import BankAccount


class BankAccountHandler:
    @staticmethod
    def get_all_count_money():
        return BankAccount.objects.aggregate(Sum('balance'))['balance__sum'], status.HTTP_200_OK
