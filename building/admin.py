from django.contrib import admin
from import_export import resources
from .models import Building, Meter, Energy


class BuildingsResource(resources.ModelResource):

    class Meta:
        model = Building


class MeterResource(resources.ModelResource):

    class Meta:
        model = Meter


class EnergyResource(resources.ModelResource):

    class Meta:
        model = Energy


admin.site.register(Building)
admin.site.register(Meter)
admin.site.register(Energy)
