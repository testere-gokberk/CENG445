from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_map/', views.create_map, name='create_map'),
    path('logout/', views.logout, name='logout'),
    path('create_component/', views.create_component, name='create_component'), 
    path("view_map/", views.view_map, name="view_map"),
    #path('view_map/<int:map_id>/', views.view_map, name='view_map'),
    path('view_map/', views.view_map, name='view_map'),
    path("list_maps/", views.list_maps, name="list_maps"),
    #path("submit_maps/", views.submit_maps, name="submit_maps"),
    path('rotate_component/', views.rotate_component, name='rotate_component'),  
    path('save_repo/', views.save_repo, name='save_repo'),  
    path('delete_component/', views.delete_component, name='delete_component'),  
    
    path('api/item-dropped/', views.item_dropped, name='item_dropped'),

]
