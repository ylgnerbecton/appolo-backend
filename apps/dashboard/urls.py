#-*- coding: utf-8 -*-

from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from apps.common.views import get_cep_json

from .views import Dashboard


urlpatterns = [
	re_path(r'^$', login_required(Dashboard.as_view()), name='dashboard'),
    path('service/cep/', get_cep_json, name="service-cep"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
