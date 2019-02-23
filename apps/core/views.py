from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from allauth.account.models import EmailAddress

from apps.core.models import Address, State, City, Neighborhood, Place
from apps.message_core.tasks import generate_number, generate_sms_confirmation
from apps.message_core.views import Sms, EmailThread
from apps.client.models import Usuario

from .forms import SignUpForm, ConfirmSmsForm, ExtraInfoForm, PhoneForm

from datetime import datetime, timedelta


"""
SIGNUP VIEW
"""
class SignUp(View):
    template_name = "sign_up.html"

    def get(self, request):
        form = SignUpForm()
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            password = request.POST.get('senha')

            usuario = form.save(commit=False)
            new_user = User.objects.create_user(username=usuario.email, email=usuario.email, password=password)
            new_user.is_active = True
            new_user.first_name = usuario.nome_completo
            new_user.save()

            usuario.user = new_user
            usuario.save()

            user = authenticate(username=usuario.email, password=password)
            if user is not None:
                login(request, user)
                
                return redirect(reverse("dashboard"))

        context = {'form':form}
        return render(request, self.template_name, context)


class ConfirmSms(View):
    template_name = "confirm_sms.html"

    def get(self, request, pk=None):
        if not pk:
            return redirect(reverse("dashboard"))

        client = Usuario.objects.get(pk=pk)

        form = ConfirmSmsForm()
        form_modal = PhoneForm()
        context = {'form':form, 'client':client, 'form_modal':form_modal}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if not pk:
            return redirect(reverse("dashboard"))

        form = ConfirmSmsForm(request.POST)
        if form.is_valid():
            # CHECK SMS CLIENT
            client = Usuario.objects.get(pk=pk)
            if client.sms_code != request.POST.get('sms_code'):
                return JsonResponse({'status': 'code_error', 'message':'Código incorreto'}, status=400)

            client.confirmation_sms = True
            client.save()

            response = {
                'status': 'success', 
                'message':'SMS confirmado com sucesso', 
                'redirect':reverse("account_extra_info", kwargs={'pk':client.pk})
            }

            return JsonResponse(response, status=200)        

        return JsonResponse({'status': 'form_error', 'message':'Favor preencher todos os campos'}, status=400)


class ReSendSms(View):
    def get(self, request, pk=None):
        try:
            client = Usuario.objects.get(pk=pk)
        except:
            return JsonResponse({'status': 'donor_error', 'message':'Usuário não encontrado'}, status=400)

        client.sms_resends = client.sms_resends + 1

        if client.sms_resends <= 1:  
            client.sms_date = datetime.now() + timedelta(minutes=5)
        else:
            client.sms_date = datetime.now() + timedelta(minutes=60)

        client.save()

        # SENDING SMS
        Sms().send(data=generate_sms_confirmation(client.phone, client.sms_code))

        response = {
            'status': 'success', 
            'message':'SMS reenviado com sucesso',
            'countdown':client.sms_date
        }
        return JsonResponse(response, status=200)


class ChangePhone(View):
    def get(self, request, pk=None):
        try:
            client = Usuario.objects.get(pk=pk)
        except:
            return JsonResponse({'status': 'client_error', 'message':'Usuário não encontrado'}, status=400)
        
        form = PhoneForm(request.GET)
        if form.is_valid():
            if client.phone == request.GET.get('phone'):
                return JsonResponse({'status': 'phone_error', 'message':'Telefone igual ao registrado'}, status=400)
                
            client.phone = request.GET.get('phone')
            client.sms_resends = 0
            client.sms_date = datetime.now() + timedelta(minutes=1)
            client.save()

            # SENDING SMS
            Sms().send(data=generate_sms_confirmation(client.phone, client.sms_code))

            response = {
                'status': 'success', 
                'message':'Telefone atualizado e SMS reenviado com sucesso',
                'countdown':client.sms_date
            }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'status': 'phone_error', 'message':'Telefone inválido'}, status=400)


class ExtraInfo(View):
    template_name = "extra_info.html"

    def get(self, request, pk=None):
        if not pk:
            return redirect(reverse("dashboard"))

        client = Usuario.objects.get(pk=pk)
        
        if client.address:
            form = ExtraInfoForm(instance=client, initial={
                'street': client.address.street,
                'number': client.address.number,
                'city': client.address.city.name,
                'neighborhood': client.address.neighborhood.description,
                'state': client.address.state.uf,
                'complement': client.address.complement,
                'reference_point': client.address.reference_point,
                'zip_code': client.address.place.zip_code,
                'latitude': client.address.city.latitude,
                'longitude': client.address.city.longitude,
                'cod_ibge': client.address.city.cod_ibge,
            })
        else:
            form = ExtraInfoForm(instance=client)   
            
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):
        if not pk:
            return redirect(reverse("dashboard"))

        client = Usuario.objects.get(pk=pk)

        form = ExtraInfoForm(request.POST, instance=client)
        if form.is_valid():
            
            state = State.objects.get_or_create(uf=request.POST.get('state'), cod_ibge=request.POST.get('cod_ibge'))[0]
            city = City.objects.get_or_create(name=request.POST.get('city'), latitude=request.POST.get('latitude'),longitude=request.POST.get('longitude'), state=state, cod_ibge=state.cod_ibge)[0]
            neighborhood = Neighborhood.objects.get_or_create(description=request.POST.get('neighborhood'), city=city)[0]
            place = Place.objects.get_or_create(zip_code=request.POST.get('zip_code'), city=city, latitude=city.latitude, longitude=city.longitude, neighborhood=neighborhood)[0]
            
            address = Address()
            address.street = request.POST.get('street')
            address.number = request.POST.get('number')
            address.complement = request.POST.get('complement')
            address.reference_point = request.POST.get('reference_point')
            address.place = place
            address.neighborhood = neighborhood
            address.city = city
            address.state = state
            address.latitude = city.latitude
            address.longitude = city.longitude
            address.save()

            # UPDATING CLIENT
            client = form.save(commit=False)
            client.address = address
            client.save()

            # ACTIVATING USER
            user = client.user
            user.is_active = True
            user.save()

            # ALLAUTH EMAIL
            try:
                auth_email = EmailAddress.objects.get(user=client.user, email=client.email)
            except:
                auth_email = EmailAddress()
                
            auth_email.user = client.user
            auth_email.email = client.email
            auth_email.save()

            # SENDING EMAIL CONFIRMATION
            auth_email.send_confirmation()

            response = {
                'status': 'success', 
                'message':'Usuário criado com sucesso', 
                'redirect':reverse("account_login")
            }

            return JsonResponse(response, status=200)

        return JsonResponse({'status': 'form_error', 'message':'Favor preencher todos os campos'}, status=400)
    
