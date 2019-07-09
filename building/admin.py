from django.contrib import admin
from .models import Building, Meter, Energy

admin.site.register(Building)
admin.site.register(Meter)
admin.site.register(Energy)
