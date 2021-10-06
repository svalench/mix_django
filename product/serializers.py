from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from product.models import Product, CardProduct, Characteristics, CharacteristicValue


class CharacteristicSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    class Meta:
        model = Characteristics
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CharacteristicValueSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    parent = CharacteristicSerializer(source='parent', read_only=True, many=True)
    class Meta:
        model = CharacteristicValue
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """сериализация модели Product """
    characteristics_norm = CharacteristicValueSerializer(source='characteristics.all', read_only=True, many=True)

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