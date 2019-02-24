from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from apps.calendar.create_event import agendar
from apps.message_core.tasks import generate_number
from apps.core.models import State, City, Neighborhood, Place, Address
from .forms import *
from .models import *
from datetime import datetime, timedelta
from time import gmtime, strftime

from pathlib import Path
import requests
import random
import re

from apps.pdf.pdf_reader import read_pdf

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

def get_user(request):
    usuario = Usuario.objects.get(user__pk=request.user.pk)
    return usuario


def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def find_between_r(s, first, last ):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        start_end = s[start:end]
        return start_end
    except ValueError:
        return ""

    
def download_pdf_day(self):
    number = random.randrange(0, 9999999)
    data_atual = strftime("%d/%m/%Y", gmtime())
    result = 'diário oficial ' + data_atual

    filename = Path('media/' + 'diario_oficial_' + str(number) + '.pdf')
    url = 'http://www.tjpe.jus.br/dje/DownloadServlet?dj=DJ39_2019-ASSINADO.PDF&amp;statusDoDiario=ASSINADO'
    response = requests.get(url, verify=False)
    filename.write_bytes(response.content)

    arq = Arquivos()
    arq.descricao = result
    arq.documento = filename.name

    doc = str(arq.documento)
    doct = 'media/' + doc
    string_pdf = read_pdf(doct)

    arq.texto = string_pdf
    arq.save()

    arq = Arquivos.objects.get(id=1)
    
    teste = arq.texto

    patt = 'Processo N'
    txts = re.split(patt, teste)
    usuario = get_user(self)

    for txt in txts:
        ato = Ato()
        ato.texto = txt
        ato.descricao = "SENTENÇA"
        ato.save()

        part_text = ato.texto
        i = part_text.find('Processo N°:')    

        processo = Processo()
        processo.usuario = usuario
        processo.texto = part_text
        processo.save()

        agendar(usuario.email, processo.texto, processo.titulo, datetime.now(), processo.data_publicacao_ato)

    # palavra_chave['Processo N°:']
    # palavra_chave['Natureza da Ação:']
    # palavra_chave['Réu:']
    # palavra_chave['Réu(s):']
    # palavra_chave['Advogado:']
    # palavra_chave['Autor:']
    # palavra_chave['Prazo']

    # processo = Processo.objects.get(id=1)
    # print(processo)
    # part = re.search('o 0000(.+?)', part_text)
    # print(part)

    return result


class Calendario(View):
    template_name = "calendario/calendario.html"

    def get(self, request):
        usuario = Usuario.objects.get(user__pk=request.user.pk)
        calendario = Processo.objects.filter(usuario=usuario)
        context = {'calendario': calendario}
        return render(request, self.template_name, context)

