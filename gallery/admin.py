from django.contrib import admin
from .models import Autore, Sala, Tema, Opera

admin.site.register([Autore, Sala, Tema, Opera])
