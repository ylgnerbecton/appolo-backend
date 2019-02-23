# DJANGO IMPORTS
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import pgettext, ugettext
from django.utils.translation import ugettext_lazy as _

# AUTH IMPORTS
from oauth2_provider.models import AccessToken, Application
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.app_settings import AuthenticationMethod
from allauth.account.forms import default_token_generator
from allauth.utils import build_absolute_uri
from allauth.account.utils import (
    filter_users_by_email, setup_user_email, user_pk_to_url_str, user_username
)

# REST IMPORTS
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

# CUSTOM IMPORTS
from apps.message_core.models import News
from apps.client.models import *
from apps.common.models import GENDER_LIST


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


'''
    AUTH SERIALIZERS
'''

class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField()

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.first_name = request.data['name']
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    cpf = serializers.SerializerMethodField()
    telefone = serializers.SerializerMethodField()
    
    def get_cpf(self, cpf): 
        return cpf

    def get_telefone(self, telefone):
        return telefone

    def validate(self, data):
        email = data['email']
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        app = Application.objects.all()
        if not self.users:
            raise serializers.ValidationError({"error":_("The e-mail address is not assigned"
                                        " to any user account"), "status": "error"})
        if not app:
            raise serializers.ValidationError({"error":_("The app is not setting"), "status": "error"})
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        if not self.users:
            raise serializers.ValidationError({"error":_("The app is not setting"), "status": "error"})
        return data


    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.validated_data['email']
        token_generator = kwargs.get("token_generator",
                                    default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)
            

            path = reverse("account_reset_password_from_key",
                        kwargs=dict(uidb36=user_pk_to_url_str(user),
                                    key=temp_key))
            url = build_absolute_uri(
                request, path)

            context = {"current_site": current_site,
                    "user": user,
                    "password_reset_url": url,
                    "request": request}
            
            if app_settings.AUTHENTICATION_METHOD \
                    != AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context)  


'''
    MESSAGE SERIALIZER
'''

class NotificationSerializer(serializers.Serializer):
    to = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)   


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ['is_removed',]


'''
    TOKEN SERIALIZER
'''

class ConvertTokenSerializer(serializers.Serializer):
    key = serializers.CharField(required=True, max_length=100)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AppRegistration(serializers.Serializer):
    registration_id = serializers.CharField(required=True, max_length=100)


'''
    USER SERIALIZER
'''

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email','first_name','last_name')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_LIST)
    celphone = serializers.CharField()

    class Meta:
        model = User
        fields = ('email','first_name','last_name','birthday','gender','celphone')