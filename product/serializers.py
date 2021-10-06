from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from product.models import Product, CardProduct


class ProductSerializer(serializers.ModelSerializer):
    """сериализация модели Product """
    class Meta:
        model = Product
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CardProductSerializer(serializers.ModelSerializer):
    """класс для Получения CardProduct"""
    child = ProductSerializer(source='child.all', read_only=True, many=True)

    class Meta:
        model = CardProduct
        permission_classes = (IsAuthenticated,)
        fields = '__all__'