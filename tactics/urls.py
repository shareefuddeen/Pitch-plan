from django.urls import path
from . import views


urlpatterns = [
    path('', views.pitch_view, name='pitch'),
    path('save/', views.save_formation, name='save_formation'),
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/<int:formation_id>/load/', views.load_formation, name='load_formation'),
    path('formations/<int:formation_id>/delete/', views.delete_formation, name='delete_formation'),
    path('formations/<int:formation_id>/rename/', views.rename_formation, name='rename_formation'),
]