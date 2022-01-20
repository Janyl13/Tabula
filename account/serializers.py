from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import User
from .tasks import send_activation_code

# User = get_user_model()

# def normalize_email(email):
#     import re
#     if re.match(r"... regex here ...", email):
#         raise serializers.ValidationError('Введите правильный email')
#     return email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        # print(validated_data)
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        print("before")
        send_activation_code.delay(email=user.email, activation_code=str(user.activation_code))
        print("after")
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')


        else:
            message = 'Must include "email" and "password"'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6)
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField(min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Укажите верный текущий пароль')
        return old_password

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_pass(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
#     def validate_email(self, email):
#         email = normalize_email(email)
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Пользователя такого нету')
#         return email



    # def send_code(self):
    #     email = self.validated_data.get('email')
    #     user = User.objects.get(email=email)
    #     user.create_activation_code()
    #     user.send_activation_code()

# class ForgotPasswordCompleteSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=6, min_length=6)
#     new_pass = serializers.CharField(min_length=6)
#     new_pass_confirm = serializers.CharField(min_length=6)
#
#     def validate_code(self, code):
#         if not User.objects.filter(activation_code=code).exists():
#             raise serializers.ValidationError('Пользователь не найден')
#         return code
#
#     def validate(self, validated_data):
#         new_pass = validated_data.get('new_pass')
#         new_pass_confirm = validated_data.get('new_pass_confirm')
#         if new_pass != new_pass_confirm:
#             raise serializers.ValidationError('Неверный пароль или его подтверждение')
#         return validated_data
#
#     def set_new_pass(self):
#         code = self.validated_data.get('code')
#         new_pass = self.validated_data.get('new_pass')
#         user = User.objects.get(activation_code=code)
#         user.set_password(new_pass)
#         user.save()

