from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (ModelSerializer,
                                        EmailField,
                                        CharField,
                                        ValidationError
                                        )
from .accounts_settings import EMAIL_HUNTER_API_KEY, CLEARBIT_API_KEY
import requests
import clearbit

clearbit.key = CLEARBIT_API_KEY

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email'
                  )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        eh_params = {
            'email': email,
            'api_key': EMAIL_HUNTER_API_KEY
        }
        email_hunter_json = requests.get('https://api.hunter.io/v2/email-verifier', params=eh_params).json()
        clearbit_json = clearbit.Enrichment.find(email=email, stream=True)
        user_obj = User(email=email,
                        username=username,
                        email_hunter_json=email_hunter_json,
                        clearbit_json=clearbit_json
                        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email',
                  'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password')
        if not username and not email:
            raise ValidationError('A username or email is required to login.')
        user = User.objects.filter(
            Q(username=username) |
            Q(email=email)
        ).distinct()
        if user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Username/email is not valid.')
        if not user_obj.check_password(password):
            raise ValidationError('Incorrect password.')
        response = requests.post('http://127.0.0.1:8000/api/token/auth/',
                                 data={'username': username, 'password': password})
        data['token'] = response.json()['token']
        return data
