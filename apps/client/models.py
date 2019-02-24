from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.common.fields import JSONField
from apps.common.models import BestPraticesModel
from apps.core.models import Address, State, City
from django.db.models.signals import post_save

import re

class Usuario(BestPraticesModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # BASIC INFO
    nome_completo = models.CharField('Nome Completo', max_length=200)
    email = models.EmailField('Email', max_length=100)
    oab = models.CharField('OAB', max_length=14, blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    
    # CONFIRMATION INFO
    sms_code = models.CharField(max_length=4, blank=True, null=True)
    sms_date = models.DateTimeField(blank=True, null=True)
    sms_resends = models.IntegerField(default=0, blank=True, null=True)
    confirmation_sms = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Usuário"
    
    def __str__(self):
        return '{}'.format(self.nome_completo)


class Arquivos(BestPraticesModel):
    descricao = models.CharField('Descrição', blank=True, null=True, max_length=200)
    documento = models.FileField('Documento', blank=True, null=True)
    texto = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Arquivos"
    
    def __str__(self):
        return '{}'.format(self.descricao)


class Ato(BestPraticesModel):
    descricao = models.CharField('Descrição', blank=True, null=True, max_length=200)
    texto = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ato"
    
    def __str__(self):
        return '{}'.format(self.descricao)


class Processo(BestPraticesModel):
    numero_processo = models.CharField(max_length=254, blank=True, null=True)
    titulo = models.CharField(max_length=254, blank=True, null=True)
    ato = models.CharField(max_length=254, blank=True, null=True)
    tipo_acao = models.CharField(max_length=254, blank=True, null=True)
    data_publicacao_ato = models.DateTimeField(blank=True, null=True)
    autor = models.CharField(max_length=254, blank=True, null=True)
    reu = models.CharField(max_length=254, blank=True, null=True)
    advogado = models.CharField(max_length=254, blank=True, null=True)
    texto = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Processo"
    
    def __str__(self):
        return '{}'.format(self.titulo)
