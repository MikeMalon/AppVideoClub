from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('login', views.userlogin, name='login'),
 path('logout', views.userlogout, name='logout'),
 path('gestion_usuarios',views.gestion_usuarios,name='gestion_usuarios'),
 path('gestion_peliculas', views.gestion_peliculas,name='gestion_peliculas'),
 path('eliminar_pelicula/<int:Pelicula_id>/',views.eliminar_pelicula,name='eliminar_pelicula'),
 path('modificar_pelicula/<int:Pelicula_id>/',views.modificar_pelicula,name='modificar_pelicula'),
 path('eliminar_usuario/<int:User_id>/',views.eliminar_usuario,name='eliminar_usuario'),
 path('modificar_usuario',views.index,name='modificar_usuario'),
 
]
