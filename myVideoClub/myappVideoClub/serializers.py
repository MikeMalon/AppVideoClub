from django.db.models import fields
from rest_framework import serializers
from myappVideoClub.models import Pelicula

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ('nombre','urlPelicula','descripcion','año','director','reparto','urlPortada','valoracion')