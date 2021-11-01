from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from catalog.models import FirstCategory, SecondCategory, DocumentsCard


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


class DocumentsCardProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsCard
        permission_classes = (AllowAny,)
        fields = '__all__'