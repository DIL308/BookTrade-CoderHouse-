from django.shortcuts import render
from .models import Libro, Categoria,Mensaje
from .forms import UserCreationFormCustom,LoginForm,UserChangeFormCustom
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
#Mix y Dec
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied




#def index(request):
#    return render(request,'index.html')

def inicio(request):
    return render(request,'inicio.html')

def aboutMe(request):
    return render(request,'acercaDeMi.html')

class SoloStaff(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

#--------------------- Usuario ---------------------#
                     
def registro_usuario(request):
          
     if request.method == "POST":
          formulario = UserCreationFormCustom(request.POST)

          if formulario.is_valid():
            data = formulario.cleaned_data
            print(data)
            username = data['username']
            formulario.save()               
            return render (request,'reg_usuario.html',{"mensaje" : f'El usuario {username} fue creado correctamente','validacion':'OK'})   
          else:
            return render(request, 'reg_usuario.html', {'mensaje' : 'Las contraseñas no coinciden o el nombre de usuario no está disponible','validacion':'Error'})
     else:
          formulario = UserCreationFormCustom()
          return render(request, 'reg_usuario.html', {'miFormulario': formulario})

@login_required
def editar_usuario(request):

    usuario = request.user

    if request.method == 'POST':
       
      Formulario = UserChangeFormCustom(request.POST, instance=request.user)

      if Formulario.is_valid():
          data = Formulario.cleaned_data
          usuario.email = data['email']
          usuario.first_name = data['first_name']
          usuario.last_name = data['last_name']
          if data["password1"]:#is_valid verifica q ambos passowrd sean =
             usuario.set_password(data["password1"])
             usuario.save()
             return render(request, "detail_user.html", {"mensaje": "¡Datos actualizados!. Vuelve a iniciar sesión"})
          usuario.save()   
          return render(request, "detail_user.html", {"mensaje": "¡Datos actualizados!"})
      else:
          return render(request, "detail_user.html", {"mensaje": "¡Las contraseñas no coinciden!"})
    else:
      Formulario = UserChangeFormCustom(instance=request.user)
      return render(request, "update_usuario.html", {"Formulario": Formulario})
    
def ingreso(request):
    
    if request.method == 'POST':
        Formulario = LoginForm(request, data=request.POST)

        if Formulario.is_valid():

          data = Formulario.cleaned_data
          username = data["username"]
          pass_word = data["password"]

          user = authenticate(username=username, password=pass_word)

          if user:
            login(request, user)
            return render(request, 'inicio.html')
          else:
            return render(request, 'inicio.html', {"mensaje": f'Error: datos incorrectos'})      

        else:
          return render(request, "inicio.html", {"mensaje": "Usuario y/o contraseña incorrectos"})
  
    else:
        Formulario = LoginForm()
        return render(request, "login.html", {"Formulario": Formulario})

class UserDetail(LoginRequiredMixin, DetailView):
  model = User
  template_name = 'detail_user.html'
  context_object_name = 'user'  
#--------------------- Categoria ---------------------#

class CreaCategoria(LoginRequiredMixin, SoloStaff, CreateView):
   model = Categoria
   template_name = 'create_category.html'
   fields = ('__all__')
   success_url = reverse_lazy('listaCategoria')

class CategoriaLista(LoginRequiredMixin, SoloStaff,ListView):
   model = Categoria
   template_name = 'list_category.html'
   context_object_name = 'categorias'
   print(context_object_name)

class CategoriaUpdate(LoginRequiredMixin, SoloStaff, UpdateView):
  model = Categoria
  template_name = 'update_category.html'
  fields = ('__all__')
  success_url = '/lista-categoria/'
  context_object_name = 'categoria'

class CategoriaDelete(LoginRequiredMixin, SoloStaff, DeleteView):
   
   model = Categoria
   template_name = 'delete_category.html'
   success_url = '/lista-categoria/'
   context_object_name = 'registro'

#--------------------- Libro ---------------------#
class CreaLibro(LoginRequiredMixin, UserPassesTestMixin, CreateView):
   model = Libro
   template_name = 'create_book.html'
   fields = ['titulo','autor','categoria','editor','precio','emailContacto','telefonoContacto','imagen','descripcion']
   success_url = reverse_lazy('listaLibro')

   def form_valid(self, form):
      form.instance.usuario = self.request.user
      return super().form_valid(form)
   def test_func(self):
        return self.request.user.is_authenticated
   
class LibroLista(ListView):
   model = Libro
   template_name = 'list_book.html'
   context_object_name = 'libros'

class LibroDetail(DetailView):
  
  model = Libro
  template_name = 'detail_book.html'
  context_object_name = 'libro'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      libro = self.get_object()
      mensajes = libro.mensaje.all()
      context['mensajes'] = mensajes
      print(f'Contexto= {context}')
      return context
  
class LibroUpdate(LoginRequiredMixin, UpdateView):
  model = Libro
  template_name = 'update_book.html'
  fields = ['titulo','autor','categoria','editor','precio','emailContacto','telefonoContacto','imagen', 'descripcion']
  success_url = '/lista-libro/'
  context_object_name = 'libro'
  
  def get_object(self, queryset=None):
      obj = super().get_object(queryset=queryset)
      if obj.usuario != self.request.user:
          raise PermissionDenied
      return obj
  
class LibroDelete(LoginRequiredMixin, DeleteView):
   
   model = Libro
   template_name = 'delete_book.html'
   success_url = '/lista-libro/'
   context_object_name = 'registro'

   def get_object(self, queryset=None):
    obj = super().get_object(queryset=queryset)
    if obj.usuario != self.request.user:
        raise PermissionDenied
    return obj

#--------------------- Mensaje ---------------------#
class Comentar(LoginRequiredMixin, CreateView):
    model = Mensaje
    fields = ['comentario']
    template_name = 'create_comment.html'
    #success_url = reverse_lazy('Inicio')
    context_object_name = 'comentario'

    def form_valid(self, form):
      libro_id = self.kwargs['pk']
      libro = get_object_or_404(Libro, pk=libro_id)
      form.instance.libro = libro
      form.instance.nombre = self.request.user
      return super().form_valid(form)
    def get_success_url(self):
      return reverse('detalleLibro', args=[self.kwargs['pk']])

#--------------------- Actualizar y Borrar ---------------------#


