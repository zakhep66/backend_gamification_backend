from django.db import models
import utils

from users.models import BankAccount


class StoreHistory(models.Model):
    store_product_id = models.ForeignKey('StoreProduct', on_delete=models.CASCADE, related_name='product')
    buyer_bank_account_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                              related_name='buyer_bank_account_id')
    date_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return self.store_product_id.product_type


class StoreProduct(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=utils.get_upload_path_for_market_image)
    price = models.PositiveIntegerField(null=False, blank=False)
    product_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'

    def __str__(self):
        return self.name
