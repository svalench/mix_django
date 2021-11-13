from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from product.models import Product, CardProduct, Characteristics, CharacteristicValue, ProductsImages, Units


class CardImagesSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    class Meta:
        model = ProductsImages
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics only"""
    class Meta:
        model = Units
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

class CharacteristicValueWithoutParentSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics only"""
    unit = serializers.SerializerMethodField()
    class Meta:
        model = CharacteristicValue
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

    def get_unit(self, obj):
        if obj.units:
            return str(obj.units.name)
        else:
            return ''


class CharacteristicSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    class Meta:
        model = Characteristics
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CharacteristicValueSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics """
    characterisitc = CharacteristicSerializer(source='parent', read_only=True)
    unit = serializers.SerializerMethodField()

    class Meta:
        model = CharacteristicValue
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

    def get_unit(self, obj):
        if obj.units:
            return str(obj.units.name)
        else:
            return ''



class CharacteristicWithValueSerializer(serializers.ModelSerializer):
    """сериализация модели Characteristics  с  CharacteristicValue"""
    val = CharacteristicValueWithoutParentSerializer(source='charac_value.all', read_only=True, many=True)
    class Meta:
        model = Characteristics
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class CardProductAlongSerializer(serializers.ModelSerializer):
    """класс для Получения CardProduct along"""

    class Meta:
        model = CardProduct
        permission_classes = (IsAuthenticated,)
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """сериализация модели Product """
    characteristics_norm = CharacteristicValueSerializer(source='characteristics.all', read_only=True, many=True)
    images = CardImagesSerializer(source='parent.images.all', read_only=True, many=True)
    img = serializers.SerializerMethodField()
    brothers = serializers.SerializerMethodField()
    characteristic_show = serializers.SerializerMethodField()
    search_filter = serializers.SerializerMethodField()
    unit_shows = serializers.SerializerMethodField()
    card = CardProductAlongSerializer(source='parent', read_only=True)

    def get_img(self, obj):
        if obj.parent:
            return str(obj.parent.img)
        else:
            return ''

    def get_brothers(self, obj):
        res = obj.parent.child.all().values()
        for i in res:
            i['value'] = i.characteristics.value
        return res

    def get_characteristic_show(self, obj):
        return obj.parent.characteristic_for_show.name

    def get_unit_shows(self, obj):
        return obj.parent.characteristic_for_show.charac_value.all().first().units.name

    def get_search_filter(self, obj):
        res = [x.characteristics.filter(parent__id=obj.parent.characteristic_for_show.id).values().first()
                for x in obj.parent.child.all()]
        return res


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