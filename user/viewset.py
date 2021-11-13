
from django.contrib.auth.hashers import check_password
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from mix_django.email import EmailSending
from user.models import User, Carts, ProductCounts
from user.serializer import UserSerializer, ChangePasswordSerializer, UserSerializerS, CartSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializerS
    permission_classes = [permissions.IsAdminUser]


class UserListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializerS
    http_method_names = ['get', 'head']
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['country', 'birth_date']
    filterset_fields = ['sex']
    search_fields = ['location', 'description', 'city', 'phone', 'qualification', 'conditions', 'country']


class DataUserViewSet(generics.RetrieveUpdateAPIView):
    """
        класс данных пользователя
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializerS

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        print(obj)
        return obj


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not check_password(request.user.password, request.data['oldPassword']):
            raise ValidationError('старый пароль не совпал')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class UserAuthTokenUpdate(ObtainAuthToken):
    """метод для обновления токена на сайте"""

    def post(self, request, *args, **kwargs):
        t = Token.objects.get(user=request.user)
        t.key = t.generate_key()
        t.save()
        return Response({
            'token': t.key,
            'user_id': request.user.pk,
            'is_admin': request.user.is_superuser,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })


class ProductCountsViewSet(viewsets.ModelViewSet):
    queryset = ProductCounts.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

class CartsViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer
    # http_method_names = ['get', 'head']
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = []
    filterset_fields = ['user_name', 'date_add', 'user_email']
    search_fields = ['user_name', 'user_email', 'user_phone']

    def perform_create(self, serializer):
        super(CartsViewSet, self).perform_create(serializer)
        email = EmailSending(self.request)
        email.send_cart_email(serializer.data)
