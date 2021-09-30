import six
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializer import UserSerializer


@api_view(['POST'])
def create_auth(request):
    """функция регистрации на сайте"""
    serialized = UserSerializer(data=request.data)

    if serialized.is_valid():
        validation_password(request.data['password'], request.data['password1'])
        u = User(
            username=serialized.validated_data['username'],
            email=serialized.validated_data['username'],
            is_active=False,
            password=make_password(serialized.validated_data['password'])
        )
        u.save()

        return Response({"OK": "OK"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


def validation_password(p, p1):
    if p != p1:
        raise ValidationError({"detail": "не верно введен пароль"})


class CustomAuthToken(ObtainAuthToken):
    """ класс описывающий  вход в систему"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            raise ValidationError({'detail': 'Вы еще не активировали аккаунт. Вход будет доступен после подтверждения '
                                             'email.'})
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = now()
        user.save()
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status.HTTP_200_OK)


class Logout(APIView):
    """ класс описывающий выход из системы"""

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_country(request):
    ip = request.GET.get('ip', None)
    if not ip:
        ip = get_client_ip(request)
    if not ip:
        return Response({'status': False, "text": "No get parameter IP"}, status=405)
    g = GeoIP2()
    try:
        country = g.country(ip)
        city = g.city(ip)
    except:
        country = g.country('beautymasters.online')
        city = g.city('beautymasters.online')
    return Response({'status': True, "text": "Good params", 'data': {"country": country, "city": city, 'ip': ip}}, status=200)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Класс генерации токена для пользователя при активации аккаунта

    """

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()
def activation_accaunt(request, uidb64, token):
    """функция активации аккаунта и перенаправления пользователя в?"""
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

