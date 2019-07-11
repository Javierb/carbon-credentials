from django.urls import path
from .views import IndexView, upload_file

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("upload/", view=upload_file, name="upload"),
]

