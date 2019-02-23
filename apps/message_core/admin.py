from django.contrib import admin

from .models import News, PushToken


admin.site.register(PushToken)
admin.site.register(News)


# Register your models here.
