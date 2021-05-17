from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('login', views.userlogin, name='login'),
 path('logout', views.userlogout, name='logout'),
 path('gestion_usuarios',views.gestion_usuarios,name='gestion_usuarios'),
 path('gestion_peliculas',views.gestion_peliculas,name='gestion_peliculas'),
 
]
