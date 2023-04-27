from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    #path('index/',index),
    path('inicio/',inicio,name='Inicio'),
    path('acerca-de-mi/',aboutMe,name='aboutMe'),
    #USUARIO
    path('registro-usuario/',registro_usuario,name='registroUsuario'),
    path('actualizar-usuario/',editar_usuario,name='actualizaUsuario'),
    path('login/',ingreso,name='Login'),
    path('logout/',LogoutView.as_view(template_name='logout.html'),name='Logout'),
    path('detalle-perfil/<pk>/',UserDetail.as_view(),name='detallePerfil'),
    #LIBRO
    path('crear-libro/',CreaLibro.as_view(),name='creaLibro'),
    path('lista-libro/',LibroLista.as_view(),name='listaLibro'),
    path('detalle-libro/<pk>/',LibroDetail.as_view(),name='detalleLibro'),
    path('actualizar-libro/<pk>/',LibroUpdate.as_view(),name='actualizaLibro'),
    path('eliminar-libro/<pk>/',LibroDelete.as_view(),name='eliminaLibro'),
    #CATEGORIA
    path('crear-categoria/',CreaCategoria.as_view(),name='creaCategoria'),
    path('lista-categoria/',CategoriaLista.as_view(),name='listaCategoria'),
    path('actualizar-categoria/<pk>/',CategoriaUpdate.as_view(),name='actualizaCategoria'),
    path('eliminar-categoria/<pk>/',CategoriaDelete.as_view(),name='eliminaCategoria'),
    #MENSAJE
    path('comentar/<pk>/',Comentar.as_view(),name='comentar'),
    #path('actualizar-comentario/<pk>/',ComentarioUpdate.as_view(),name='actualizaComentario'),
]