
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context and self.context['request'].method == "PUT":
            self.fields.pop('password')
            self.fields.pop('username')
        if 'request' in self.context and self.context['request'].method == "GET":
            self.fields.pop('password')

    class Meta:
        model = User
        permission_classes = (IsAuthenticated,)
        fields = '__all__'

    def update(self, instance, validated_data):
        token = Token.objects.get(user_id=instance.id)
        if token != self.context['request'].auth:
            raise ValidationError(detail={"detail": "не верный токен. Пройдите авторизацию по новой!"})
        super(UserSerializer, self).update(instance, validated_data)
        instance.set_password(make_password(instance.password))
        if self.context['request'].method != "PUT":
            instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Класс предназначен для обновления пароля пользователя
    Вводится новый  пароль password  подтверждение пароля password2  и старый пароль old_password
    """
    # password = serializers.CharField(write_only=True, required=True, validators=[validators.validate_password])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializerS(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializerS, self).__init__(*args, **kwargs)
        if 'request' in self.context and self.context['request'].method == "GET":
            self.fields.pop('password')
            self.fields.pop('user_permissions')


    class Meta:
        model = User
        permission_classes = (IsAuthenticated,)
        fields = '__all__'
