"""appolo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views import defaults as default_views
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

admin.site.site_header = settings.ADMIN_SITE_HEADER

schema_view = get_swagger_view(title='API')

urlpatterns = [
    re_path(r'^$', RedirectView.as_view(pattern_name='dashboard', permanent=False)),

    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include('apps.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # AUTH
    # path('accounts/', include('allauth.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # CUSTOM
    path('', include('apps.core.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('dashboard/client/', include('apps.client.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('swagger/', schema_view)
]