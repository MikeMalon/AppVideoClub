from django.db import models

# Create your models here.
class Pelicula(models.Model):
    nombre = models.CharField(max_length=50)
    urlPelicula = models.URLField(max_length=200)
    descripcion = models.CharField(max_length=100)
    año = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    reparto = models.CharField(max_length=50)
    urlPortada = models.URLField(max_length=100)
    valoracion = models.CharField(max_length=50)