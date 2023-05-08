from rest_framework import serializers

from market.models import StoreProduct, StoreHistory


class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = '__all__'


class StoreHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHistory
        fields = '__all__'


class IssuedStoreHistorySerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='store_product_id.id')
    product_name = serializers.CharField(source='store_product_id.name')
    product_description = serializers.CharField(source='store_product_id.description')
    product_image = serializers.ImageField(source='store_product_id.image')
    student_id = serializers.IntegerField(source='buyer_bank_account_id.student.id')
    student_first_name = serializers.CharField(source='buyer_bank_account_id.student.first_name')
    student_last_name = serializers.CharField(source='buyer_bank_account_id.student.last_name')
    date_time = serializers.DateTimeField()

    class Meta:
        model = StoreHistory
        fields = ('product_id', 'product_name', 'product_description', 'product_image', 'student_id', 'student_first_name', 'student_last_name', 'date_time')


