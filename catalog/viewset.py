from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from catalog.models import FirstCategory
from catalog.serializers import CategoriesSerializer


class CategoriesListViewSet(viewsets.ModelViewSet):
    queryset = FirstCategory.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = []
    search_fields = ['name']