from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django_extensions.db.models import TimeStampedModel
from model_utils.models import SoftDeletableModel

import re


class BestPraticesModel(SoftDeletableModel):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


GENDER_LIST = (
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino'),
)

CIVIL_STATUS_LIST = (
    ('Solteiro(a)', 'Solteiro(a)'),
    ('Casado(a)', 'Casado(a)'),
    ('Viúvo(a)', 'Viúvo(a)'),
    ('Divorciado(a)', 'Divorciado(a)'),
    ('Outro', 'Outro'),
)