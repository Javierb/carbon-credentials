from django.urls import path
from .views import BuildingListView, MeterListView, EnergyListView, upload_file

urlpatterns = [
    path("", view=BuildingListView.as_view(), name="home"),
    path('meter/<int:building_id>/', view=MeterListView.as_view(), name="meter-list"),
    path("energy/<int:meter_id>/", view=EnergyListView.as_view(), name="energy-list"),
    path("upload/", view=upload_file, name="upload"),
]
