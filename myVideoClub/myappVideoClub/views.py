

from decimal import Context
from re import search
from django.db.models import query
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
import requests
from myappVideoClub import models
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from myappVideoClub.serializers import *
import tmdbsimple as tmdb
import json



@login_required(login_url='login')
def index(request):
   pelis = models.Pelicula.objects.all()
   for p in pelis:
      nombre1 = p.nombre
      nombre = nombre1.replace(' ','%20')
      search = ' https://api.themoviedb.org/3/search/movie?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES&query=' + nombre + '&page=1&include_adult=false' 
      info = requests.get(search)
      #info = requests.get('https://api.themoviedb.org/3/movie/'  +  + '?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES')
   path = 'https://image.tmdb.org/t/p/original'
   info2 = info.json()
   info21 = info2['results']
   context = {
     'peliculas' : models.Pelicula.objects.all(),
     'nombres' : models.Pelicula.objects.values('nombre'),
     'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
     'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
     'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
     'can_add_users'    : request.user.has_perm('auth.add_user'),
     'can_change_users' : request.user.has_perm('auth.change_user'),
     'can_delete_users' : request.user.has_perm('auth.delete_user'),
     #'descripcion' : info21[0]['overview'],
     #'año': info21[0]['release_date'],
     #'director': info2[''],
     #'reparto' : info2[''],
     #'valoracion' : info21[0]['vote_average'],
     #'urlPortada' : path + info21[1]['poster_path'],
   }
   return render(request, 'myappVideoClub/index.html',context)

def api_request(request,Pelicula_nombre):
   pelis = models.Pelicula.objects.filter(nombre=Pelicula_nombre)
   nombre1 = Pelicula_nombre
   nombre = nombre1.replace(' ','%20')
   search = 'https://api.themoviedb.org/3/search/movie?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES&query=' + nombre + '&page=1&include_adult=false' 
   info = requests.get(search)
   #info = requests.get('https://api.themoviedb.org/3/movie/'  +  + '?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES')
   path = 'https://image.tmdb.org/t/p/w500'
   info2 = info.json()
   info21 = info2['results']
   for p in pelis:
      contador = 0
      for i in info21: 
         if(info2['total_pages'] != 0 and info21[contador]['poster_path'] != None and info21[contador]['original_title'] != None and info21[contador]['overview'] != None and info21[contador]['release_date'] != None and info21[contador]['vote_average'] != None):
            p.nombre = info21[contador]['original_title']
            p.descripcion = info21[contador]['overview']
            p.año = info21[contador]['release_date']
            #p.director = info21[contador]['']
            #p.reparto = info21[contador]['']
            p.valoracion = info21[contador]['vote_average']
            p.urlPortada = path + info21[contador]['poster_path']
            p.save()
            break
         else:
            contador = contador + 1
   return redirect('index')

def pelicula(request,Pelicula_id):
   pelis = models.Pelicula.objects.filter(id=Pelicula_id)
   nombre1 = ""
   for pe in pelis:
      nombre1 = pe.nombre
   nombre = nombre1.replace(' ','%20')
   search = 'https://api.themoviedb.org/3/search/movie?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES&query=' + nombre + '&page=1&include_adult=false' 
   info = requests.get(search)
   #info = requests.get('https://api.themoviedb.org/3/movie/'  +  + '?api_key=1ade8415b093864d65de28be8252ec92&language=es-ES')
   path = 'https://image.tmdb.org/t/p/w500'
   info2 = info.json()
   info21 = info2['results']
   for p in pelis:
      contador = 0
      for i in info21: 
         if(info2['total_pages'] != 0 and info21[contador]['poster_path'] != None and info21[contador]['original_title'] != None and info21[contador]['overview'] != None and info21[contador]['release_date'] != None and info21[contador]['vote_average'] != None):
            p.nombre = info21[contador]['original_title']
            p.descripcion = info21[contador]['overview']
            p.año = info21[contador]['release_date']
            #p.director = info21[contador]['']
            #p.reparto = info21[contador]['']
            p.valoracion = info21[contador]['vote_average']
            p.urlPortada = path + info21[contador]['poster_path']
            p.save()
            break
         else:
            contador = contador + 1
   context = {
      'peliculas' :  models.Pelicula.objects.filter(id=Pelicula_id),
      'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
      'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
      'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
      'can_add_users'    : request.user.has_perm('auth.add_user'),
      'can_change_users' : request.user.has_perm('auth.change_user'),
      'can_delete_users' : request.user.has_perm('auth.delete_user'),
   }
   return render(request,'myAppVideoClub/pelicula.html',context)




@login_required(login_url='login')
def gestion_usuarios(request):
   if request.method == 'GET':
      context = {
         'usuarios': User.objects.all(),
         'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
         'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
         'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
         'can_add_users'    : request.user.has_perm('auth.add_user'),
         'can_change_users' : request.user.has_perm('auth.change_user'),
         'can_delete_users' : request.user.has_perm('auth.delete_user'),
      }
      return render(request,'myappVideoClub/gestion_usuarios.html',context)
   elif request.method == 'POST':
      nombre = request.POST['nombre']
      contraseña = request.POST['contraseña']
      correo = request.POST['correo']
      nuevoUsuario = User.objects.create_user(nombre,correo,contraseña)
      nuevoUsuario.save()
      return redirect('gestion_usuarios')

@login_required(login_url='login')
def gestion_peliculas(request):
   if request.method == 'GET':
      context = {
         'peliculas': models.Pelicula.objects.all(),
         'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
         'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
         'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
         'can_add_users'    : request.user.has_perm('auth.add_user'),
         'can_change_users' : request.user.has_perm('auth.change_user'),
         'can_delete_users' : request.user.has_perm('auth.delete_user'),
      }
      return render(request,'myappVideoClub/gestion_peliculas.html',context)
   elif request.method == 'POST':
      nombrePeli = request.POST['nombre']
      urlPeli = request.POST['urlPeli']
      descripcion = request.POST['descripcion']
      año = request.POST['año']
      director = request.POST['director']
      reparto = request.POST['reparto']
      urlPortada = request.POST['urlPortada']
      valoracion = request.POST['valoracion']
      nuevaPeli = models.Pelicula(nombre=nombrePeli,urlPelicula=urlPeli,descripcion=descripcion,año=año,director=director,reparto=reparto,urlPortada=urlPortada,valoracion=valoracion)
      nuevaPeli.save()
      return redirect('gestion_peliculas')

@login_required(login_url='login')
def eliminar_pelicula(request,Pelicula_id):
   peliculas = models.Pelicula.objects.filter(id=Pelicula_id)
   for p in peliculas:
      p.delete()
   return redirect('gestion_peliculas') #Volvemos a la pantalla principal de las peliculas del administrador

@login_required(login_url='login')
def eliminar_usuario(request,User_id):
   usuarios = User.objects.filter(id=User_id)
   for u in usuarios:
      u.delete()
   return redirect('gestion_usuarios') #Volvemos a la pantalla principal de los usuarios del administrador

def modificar_pelicula(request,Pelicula_id):
   peliculas = models.Pelicula.objects.filter(id=Pelicula_id)
   nombrePeli = request.POST['nombre']
   urlPeli = request.POST['urlPeli']
   descripcion = request.POST['descripcion']
   año = request.POST['año']
   director = request.POST['director']
   reparto = request.POST['reparto']
   urlPortada = request.POST['urlPortada']
   valoracion = request.POST['valoracion']
   for p in peliculas:
      p.nombre = nombrePeli
      p.urlPeli = urlPeli
      p.descripcion = descripcion
      p.año = año
      p.director = director
      p.reparto = reparto
      p.urlPortada = urlPortada
      p.valoracion = valoracion
      p.save()
   return redirect('gestion_peliculas')

def modificar_usuario(request,User_id):
   usuarios = User.objects.filter(id=User_id)
   nombre = request.POST['nombre']
   contraseña = request.POST['contraseña']
   correo = request.POST['correo']
   for u in usuarios:
      u.username = nombre
      u.set_password = contraseña
      u.email = correo
      u.save()
   return redirect('gestion_usuarios')


   
   #tmdb.API_KEY="1ade8415b093864d65de28be8252ec92"
   #busqueda = tmdb.Search()
   #respuesta = busqueda.movie(query=Pelicula_nombre)
   #descripcion = ""
   #for r in respuesta.results:
      #descripcion = r['overview']
   #for p in peliculas:
      #p.descripcion = descripcion   
   #return render(request,'myappVideoClub/index',context={'apiP' : peliculas}) 


      



def userlogin(request):
   if request.method == 'GET':
      return render(request,'myappVideoClub/login.html',{})
   elif request.method == 'POST':
      nombre = request.POST['nombre']
      contraseña = request.POST['contraseña']
      user = authenticate(request, username = nombre,password = contraseña)
      if user is not None:
         login(request,user)
         return redirect('index')
      else:
         return render(request,'myappVideoClub/login.html',{'login_failed':True})

@login_required(login_url='login')
def userlogout(request):
   logout(request)    
   return redirect('login') 





