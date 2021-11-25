from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from mix_django.email import EmailSending
from product.models import Product, CharacteristicValue, Characteristics, CardProduct
from product.serializers import ProductSerializer, CharacteristicValueSerializer, CharacteristicWithValueSerializer, \
    CardProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q


class ProductsListRandomViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['parent__category', 'characteristics']
    search_fields = ['name', 'article']

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def get_queryset(self):
        return Product.objects.order_by('?')

class ProductsListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['parent__category', 'characteristics', 'parent']
    search_fields = ['name', 'article']

        
    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        super(ProductsListViewSet, self).get_queryset()
        filter_values = []
        if self.request.GET.get('filter_ch'):
            filter_values = self.request.query_params.getlist('filter_ch')
            charac = Characteristics.objects.filter(charac_value__id__in=filter_values)
            for ch in charac:
                qq = Q()
                for c in ch.charac_value.all():
                    if str(c.id) in filter_values:
                        print(c.id, c.value, ch.id, ch.name)
                        qq = qq | Q(characteristics__id=c.id)
                queryset = queryset.filter(qq)
        return queryset


class CharacteristicsByCatListViewSet(viewsets.ModelViewSet):
    queryset = CharacteristicValue.objects.all()
    serializer_class = CharacteristicValueSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['characteristic__parent__category']
    search_fields = ['name', 'article']


class CharacteristicsListViewSet(viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicWithValueSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['charac_value__characteristic__parent__category']
    search_fields = ['name', 'article']

class CardProductViewSet(viewsets.ModelViewSet):
    queryset = CardProduct.objects.all()
    serializer_class = CardProductSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = []
    search_fields = ['name', 'child__name']