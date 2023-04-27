from django.contrib import admin
from .models import Libro, Categoria,Mensaje

# Register your models here.


admin.site.register(Libro)
admin.site.register(Categoria)
admin.site.register(Mensaje)
