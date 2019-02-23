from django.contrib import admin

from .models import Address, City, Neighborhood, Place, State, Company

admin.site.register(Address)
admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(State)
admin.site.register(Place)
admin.site.register(Company)