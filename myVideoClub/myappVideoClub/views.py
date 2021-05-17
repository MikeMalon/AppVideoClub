
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from myappVideoClub import models


@login_required(login_url='login')
def index(request):
   context = {
     'peliculas' : models.Pelicula.objects.all(),
     'nombres' : models.Pelicula.objects.values('nombre'),
     'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
     'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
     'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
     'can_add_users'    : request.user.has_perm('auth.add_user'),
     'can_change_users' : request.user.has_perm('auth.change_user'),
     'can_delete_users' : request.user.has_perm('auth.delete_user'),
   }
   return render(request, 'myappVideoClub/index.html',context)

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





