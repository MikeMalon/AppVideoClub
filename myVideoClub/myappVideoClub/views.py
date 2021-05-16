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
     'can_add_pelis' : request.user.has_perm('myappVideoClub.add_pelicula'),
     'can_change_pelis' : request.user.has_perm('myappVideoClub.change_pelicula'),
     'can_delete_pelis' : request.user.has_perm('myappVideoClub.delete_pelicula'),
   }
   return render(request, 'myappVideoClub/index.html',context)

def gestion_usuarios(request):
   if request.method == 'GET':
      context = {
         'usuarios': User.objects.all()
      }
      return render(request,'myappVideoClub/gestion_usuarios.html',context)
   elif request.method == 'POST':
      nombre = request.POST['nombre']
      contraseña = request.POST['contraseña']
      correo = request.POST['correo']
      nuevoUsuario = User.objects.create_user(nombre,contraseña,correo)
      nuevoUsuario.save()
      return redirect('gestion_usuarios')
      

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





