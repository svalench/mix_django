from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from catalog.models import FirstCategory, DocumentsCard, SecondCategory
from catalog.serializers import CategoriesSerializer, DocumentsCardProductSerializer, SecondCategorySerializer


class CategoriesListViewSet(viewsets.ModelViewSet):
    queryset = FirstCategory.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['weight_in_menu']
    filterset_fields = []
    search_fields = ['name']

class CategoriesSecondListViewSet(viewsets.ModelViewSet):
    queryset = SecondCategory.objects.all()
    serializer_class = SecondCategorySerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = []
    search_fields = ['name']


class DocsCertificatesViewSet(viewsets.ModelViewSet):
    """
    API для админки сертификатов
    """
    queryset = DocumentsCard.objects.all()
    http_method_names = ['get', 'head']
    serializer_class = DocumentsCardProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['parent']
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset = DocumentsCard.objects.all()
        super(DocsCertificatesViewSet, self).get_queryset()
        filter_values = []
        if self.request.GET.get('parent_ch'):
            filter_values = self.request.query_params.getlist('parent_ch')
            qq = Q(parent__in=filter_values)
            queryset = queryset.filter(qq)
        return queryset
