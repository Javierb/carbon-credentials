from django.urls import path, include
from .views import BuildingListView, MeterListView, EnergyListView, upload_file, DataView
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path("", view=BuildingListView.as_view(), name="home"),
    path('meter/<int:building_id>/', view=MeterListView.as_view(), name="meter-list"),
    path("energy/<int:meter_id>/", view=EnergyListView.as_view(), name="energy-list"),
    path("upload/", view=upload_file, name="upload"),
    path('api/daily-data/<int:meter_id>/', view=DataView.as_view()),
    path('api/', include(router.urls)),
]
