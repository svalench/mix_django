from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from catalog.models import FirstCategory, DocumentsCard
from catalog.serializers import CategoriesSerializer, DocumentsCardProductSerializer


class CategoriesListViewSet(viewsets.ModelViewSet):
    queryset = FirstCategory.objects.all()
    serializer_class = CategoriesSerializer
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
    permission_classes = [permissions.AllowAny]
