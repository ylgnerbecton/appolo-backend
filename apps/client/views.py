from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.db.models import Q

from apps.message_core.tasks import generate_number
from apps.core.models import State, City, Neighborhood, Place, Address
from .forms import *
from .models import *
from datetime import datetime, timedelta

from apps.pdf.pdf_reader import read_pdf



class PDFToText(View):
    template_name = "usuario/list.html"

    def get(self, request):
        arquivo = Arquivos.objects.get(pk=1)
        doc = str(arquivo.documento)
        doct = 'media/' + doc
        print(doct)
        string_pdf = read_pdf(doct)
        
        print(string_pdf)

        # pdfFileObj = open('media/Smart_Cities_A_Survey_on_Data_Management.pdf', 'rb') 
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        # pageObj = pdfReader.getPage(0) 
        # string_pdf = pageObj.extractText()
        # print(string_pdf)
        # pdfFileObj.close()

        arquivo.texto = string_pdf
        arquivo.save(update_fields=["texto"]) 

        context = {'arquivo': arquivo}
        return render(request, self.template_name, context)



"""
USUARIO VIEW
"""
class UsuarioList(View):
    template_name = "usuario/list.html"

    def get(self, request):
        usuario = Usuario.objects.all()
        context = {'usuario': usuario}
        return render(request, self.template_name, context)


class UsuarioCreate(View):
    template_name = "usuario/create.html"

    def get(self, request):
        form = UsuarioForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.save(commit=False)
            new_user = User.objects.create_user(username=usuario.email, email=usuario.email, password='apenasum2019')
            new_user.is_active = True
            new_user.first_name = usuario.nome_completo
            new_user.save()

            usuario.user = new_user
            usuario.save()

            return redirect(reverse("usuario-list"))

        context = {'form':form}
        return render(request, self.template_name, context)


class UsuarioEdit(View):
    template_name = "usuario/edit.html"

    def get(self, request, pk):
        usuario = Usuario.objects.get(pk=pk)
        form = UsuarioForm(instance=usuario)
        context = {'form': form, 'usuario':usuario}
        return render(request, self.template_name, context)

    def post(self, request, pk):    
        usuario = Usuario.objects.get(pk=pk)
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            
            return redirect(reverse("usuario-list"))

        context = {'form':form, 'usuario':usuario}
        return render(request, self.template_name, context)


class UsuarioDelete(View):
    def get(self, request, pk):
        Usuario.objects.get(pk=pk).delete()
        return redirect(reverse("usuario-list"))

class ProcessoList(View):
    template_name = "processo/list.html"

    def get(self, request):
        processo = Processo.objects.all()
        context = {'processo': processo}
        return render(request, self.template_name, context)
