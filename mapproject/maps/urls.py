from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_map/', views.create_map, name='create_map'),
    path('logout/', views.logout, name='logout'),
    path('create_component/', views.create_component, name='create_component'),  # Add the create_component URL
    path('delete_component/', views.delete_component, name='delete_component'),  # Add the create_component URL

]
