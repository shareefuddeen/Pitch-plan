from django.urls import path
from . import views

urlpatterns =[
    path("", views.pitch_view, name="pitch"),
  
]