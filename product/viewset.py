from product.models import Product, CharacteristicValue, Characteristics
from product.serializers import ProductSerializer, CharacteristicValueSerializer, CharacteristicWithValueSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductsListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['parent__category', 'characteristics']
    search_fields = ['name', 'article']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        super(ProductsListViewSet, self).get_queryset()
        filter_values = []
        print(self.request.query_params)
        print(self.request.GET)
        if self.request.GET.get('filter_ch'):
            if not isinstance(self.request.GET.get('filter_ch'), list):
                filter_values = [self.request.GET.get('filter_ch')]
            else:
                filter_values = self.request.GET.get('filter_ch')
            charac = CharacteristicValue.objects.filter(id__in=filter_values).values_list('id')
            for ch in filter_values:
                print(ch)
                queryset.filter(characteristics=ch)
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
