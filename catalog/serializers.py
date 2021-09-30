from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from catalog.models import FirstCategory, SecondCategory


class SecondCategorySerializer(serializers.ModelSerializer):
    """сериализация модели вложенных категорий"""
    class Meta:
        model = SecondCategory
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """класс для Получения категорий с вложенными подкатегориями"""
    child = SecondCategorySerializer(source='child.all', read_only=True, many=True)

    class Meta:
        model = FirstCategory
        permission_classes = (IsAuthenticated,)
        fields = '__all__'