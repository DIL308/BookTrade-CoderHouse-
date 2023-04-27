from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
       return self.nombre

class Libro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    editor = models.CharField(max_length=50,null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    emailContacto = models.EmailField(verbose_name='Email')
    telefonoContacto = models.IntegerField(verbose_name='Teléfono')
    imagen = models.ImageField(upload_to="imagenlibros/")
    descripcion = models.CharField(max_length=100,null=True, blank=True,verbose_name='Descripción')
    fechaPublicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return '%s - %s' % (self.titulo, self.autor)
    
class Mensaje(models.Model):
    libro = models.ForeignKey(Libro, related_name='mensaje', on_delete=models.CASCADE, null=True)
    nombre = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fechaMensaje = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return '%s - %s' % (self.nombre, self.comentario)