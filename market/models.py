from django.db import models
from django.db.models import Q

import utils

from users.models import BankAccount, Student


class StoreHistory(models.Model):
    store_product_id = models.ForeignKey('StoreProduct', on_delete=models.CASCADE, related_name='product')
    buyer_bank_account_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                              related_name='buyer_bank_account_id')
    date_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'История покупки'
        verbose_name_plural = 'История покупок'

    def __str__(self):
        return self.store_product_id.product_type


class StoreProduct(models.Model):
    PRODUCT_TYPE = (
        ('merch', 'merch'),
        ('back_color', 'back_color'),
        ('emoji', 'emoji')
    )

    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=utils.get_upload_path_for_market_image)
    price = models.PositiveIntegerField(null=False, blank=False)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE)
    in_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    @staticmethod
    def get_available_products_for_student(student_id: int):
        """
        Возвращает список товаров, которые может купить студент
        """
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            # Handle the case where the student doesn't exist
            return StoreProduct.objects.none()

        bought_non_merch_products = StoreHistory.objects.filter(
            buyer_bank_account_id__student__id=student_id
        ).exclude(
            store_product_id__product_type='merch'
        ).values_list('store_product_id', flat=True)

        available_products = StoreProduct.objects.exclude(
            Q(id__in=bought_non_merch_products) & ~Q(product_type='merch')
        ).filter(
            in_stock=True
        )
        return available_products
