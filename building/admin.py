from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Building, Meter, Energy
from .resources import BuildingsResource, MeterResource, EnergyResource


@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingsResource

@admin.register(Meter)
class MeterAdmin(ImportExportModelAdmin):
    resource_class = MeterResource

@admin.register(Energy)
class EnergyAdmin(ImportExportModelAdmin):
    resource_class = EnergyResource

# admin.site.register(Building)
# admin.site.register(Meter)
# admin.site.register(Energy)
