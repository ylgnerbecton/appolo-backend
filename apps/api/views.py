from django.dispatch import Signal
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

# AUTH IMPORTS
from allauth.account.utils import filter_users_by_email
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken, Application, get_access_token_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from oauthlib import common

from django.contrib.auth import authenticate, login, logout

# REST IMPORTS
from rest_auth.registration.views import RegisterView, SocialLoginView
from rest_framework import filters, generics, pagination, mixins
from rest_framework.authtoken.models import Token as Auth_Token
from rest_framework.views import APIView, Response

# CUSTOM IMPORTS
from django.contrib.auth.models import User
from apps.client.models import *
from apps.common.views import get_address
from apps.message_core.models import PushToken
from apps.message_core.tasks import generate_number
from datetime import datetime, timedelta
from . import serializers
import json
import requests

app_authorized = Signal(providing_args=["request", "token"])


class CustomPageNumberPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'pagination': {
                'actual_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'start_index': self.page.start_index(),
                'end_index': self.page.end_index(),
            },
            'results': data
        })


class BestPraticsList(object):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    pagination_class = CustomPageNumberPagination


'''
    AUTH VIEWS
'''

class ResetPassword(APIView):
    serializer_class = serializers.ResetPasswordSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SignUp(RegisterView, OAuthLibMixin):
    serializer_class = serializers.SignUpSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if hasattr(request.data, "_mutable"):
            request.data._mutable = True
        request.data.update({"password": request.data['password1']})
        body, status = oauth2_login(self, request, serializer)
        return Response(body,
                        status=status,
                        headers=headers)


class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        context = {}
        serializer = serializers.LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            try:
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
            except:
                pass

            try:
                app = Application.objects.all()[0]
            except:
                context['msg'] = 'Application não encontrado'
                return Response(context, status=500)
            
            if user:
                try:
                    usuario = Usuario.objects.get(user__id=user.id)
                except:
                    pass
                
                try:
                    context = {
                        'name': usuario.nome_completo,
                        'email': usuario.email,
                        'cpf': usuario.cpf,
                        'telefone': usuario.telefone
                    }
                except:
                    pass

                return Response(context, status=200)
            else:
                context['status'] = 'incorrectPassword'
                context['msg'] = 'Senha incorreta.'
                return Response(context, status=409)

            return Response(context, status=200)
        else:
            return Response(serializer.errors, status=500)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


'''
    MESSAGE VIEWS
'''
class SendPushNotification(APIView):
    def post(self, request, format=None):
        serializer = serializers.NotificationSerializer(data=request.data)
        message = {}

        if serializer.is_valid():
            headers = {'Content-Type': 'applications/json', 'Accept': 'applications/json'}
            url = 'https://exp.host/--/api/v2/push/send'

            payload = json.dumps({
                'to': 'ExponentPushToken[%s]' % (serializer.data['to']),
                'title': serializer.data['title'],
                'body': serializer.data['body']
            })
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code >= 200 and response.status_code < 300:
                message = {'status': 'success', 'message': 'Notification sended'}
                return Response(message, 200)
            else:
                return Response(response, 400)
        return Response(message, 400)


'''
    TOKEN VIEWS
'''

class ConvertToken(generics.GenericAPIView):
    serializer_class = serializers.ConvertTokenSerializer

    def post(self, request):
        message = {}
        serializer = serializers.ConvertTokenSerializer(data=request.data)
        if serializer.is_valid():
            application = Application.objects.all()[0]
            token = Auth_Token.objects.get(key=serializer.data['key'])
            expires = datetime.now() + timedelta(days=180)
            access_token = AccessToken(
                user=token.user,
                scope='read write groups',
                expires=expires,
                token=common.generate_token(),
                application=application
            )
            access_token.save()
            message['access_token'] = access_token.token
            message['expires_in'] = 3600
            message['token_type'] = "Bearer"
            message['scope'] = access_token.scope
            message['refresh_token'] = access_token.token

            return Response(message, 200)
        else:
            message['status'] = 'error'
            return Response(message, 500)


class RefreshToken(BestPraticsList, OAuthLibMixin, generics.GenericAPIView):
    serializer_class = serializers.RefreshTokenSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def get(self, request, format=None):
        serializer = serializers.RefreshTokenSerializer()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            app = Application.objects.all()[0]
            request.data.update(
                {"grant_type": "refresh_token", "client_id": app.client_id, "client_secret": app.client_secret})
            url, headers, body, status = self.create_token_response(request)
            if status == 200:
                access_token = json.loads(body).get("access_token")
                if access_token is not None:
                    token = get_access_token_model().objects.get(
                        token=access_token)
                    app_authorized.send(
                        sender=self, request=request,
                        token=token)
            response = HttpResponse(content=body, status=status)
            for k, v in headers.items():
                response[k] = v
            return Response(json.loads(body), status=200)
        return Response(serializer.errors, status=400)


class AppRegistrationAPI(generics.GenericAPIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = serializers.AppRegistration

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        response = {}
        if serializer.is_valid():
            token = PushToken.objects.filter(token=serializer.data['registration_id'])
            if token:
                push_token = token[0]
                push_token.user = self.request.user
                push_token.save()
            else:
                push_token = PushToken()
                push_token.token = serializer.data['registration_id']
                push_token.user = self.request.user
                push_token.save()
            return Response(response, status=200)
        return Response(response, status=500)


'''
    User VIEWS
'''

class Profile(generics.GenericAPIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.ProfileUpdateSerializer
        else:
            return serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            user.first_name = serializer.data['first_name']
            user.last_name = serializer.data['last_name']
            user.save()
            return Response({}, status=200)
        return Response(serializer.errors, status=400)


class AddressAPI(APIView):
    def get(self, request, cep):
        response = get_address(cep)
        return response
