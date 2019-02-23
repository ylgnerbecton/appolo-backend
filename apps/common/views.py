import random
import string
from datetime import date, datetime, timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

import requests
from dateutil.relativedelta import relativedelta
from django_filters.views import FilterView

from django.template.loader import get_template
from django.http import HttpResponse

class GenericFilterList(FilterView):
    template_name_suffix = '_list'
    model = None
    template_filter_name = None
    filterset_class = None
    list_display = None
    verbose_name = None
    verbose_name_plural = None

    def get_context_data(self, **kwargs):
        context = super(GenericFilterList, self).get_context_data(**kwargs)  # get the default context data
        if self.template_filter_name:
            context['template_filter_name'] = self.template_filter_name  # add extra field to the context
        if self.model:
            if self.verbose_name:
                context['verbose_name'] = self.verbose_name
            else:
                context['verbose_name'] = self.model._meta.verbose_name
            if self.verbose_name_plural:
                context['verbose_name_plural'] = self.verbose_name_plural
            else:
                context['verbose_name_plural'] = self.model._meta.verbose_name_plural
            if self.list_display:
                list_display_names = []
                for field in self.list_display:
                    try:
                        verbose_name = self.model._meta.get_field(field).verbose_name
                    except:
                        verbose_name = field
                    list_display_names.append(verbose_name)
                context['list_display_names'] = list_display_names  # add extra field to the context
        return context


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


def get_address(cep):
    request = requests.get(
        'http://www.cepaberto.com/api/v2/ceps.json?cep=' + cep,
        headers={'Authorization': 'Token token=055cc8e8b0e25d6b6bb30a6dad8b1932'})
    response = request.json()
    return JsonResponse(response, status=request.status_code)


def get_cep_json(request):
    if request.method == 'GET':
        response = get_address(request.GET.get('cep'))
    elif request.method == 'POST':
        response = get_address(request.POST.get('cep'))
    return response


class ModelMetric():
    def get_metric(self,queryset,range):
        response = int()
        if range == 'today':
            response = queryset.filter(created__date=datetime.now().date()).count()
        if range == 'yesterday':
            date_metric = (datetime.now() - timedelta(days=1)).date()
            response = queryset.filter(created__date=date_metric).count()
        if range == 'last_week':
            date_metric = (datetime.now() - timedelta(weeks=1)).date()
            response = queryset.filter(created__date__gte=date_metric).count()
        if range == 'last_month':
            date_metric = (datetime.now() - relativedelta(months=1)).date()
            response = queryset.filter(created__date__gte=date_metric).count()
        if range == 'last_year':
            date_metric = (datetime.now() - relativedelta(year=1)).date()
            response = queryset.filter(created__date__gte=date_metric).count()
        return response

    def get_all_metrics(self, queryset):
        response = {}
        list_metrics = ['today', 'yesterday','last_week','last_month','last_year']
        for metric in list_metrics:
            response[metric] = self.get_metric(queryset,metric)
        response['all'] = queryset.count()
        return response

    def get_status_metrics(self, queryset, status_list):
        response = []
        for status in status_list:
            response.append({'name': status, 'metrics': self.get_all_metrics(queryset.filter(status=status))})
        return response

    def ranking(self, queryset, value):
        return queryset.order_by('-modified')[:value]


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]