from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from product.models import Product, CardProduct, Characteristics, CharacteristicValue, ProductsImages


class CardImagesSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    class Meta:
        model = ProductsImages
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

class CharacteristicSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    class Meta:
        model = Characteristics
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CharacteristicValueSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    characterisitc = CharacteristicSerializer(source='parent', read_only=True)
    class Meta:
        model = CharacteristicValue
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """сериализация модели Product """
    characteristics_norm = CharacteristicValueSerializer(source='characteristics.all', read_only=True, many=True)
    images = CardImagesSerializer(source='parent.images.all', read_only=True, many=True)
    # img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.parent:
            return obj.parent.img
        else:
            return None

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