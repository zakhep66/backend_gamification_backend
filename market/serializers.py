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
