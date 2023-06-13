from django.urls import path
from .instructorViews import Inicio_sesion,NombreInstructor,InstructorDestroy,BuscadorInstructor,salir,instructoresDisponiblesFecha,InstructoresListAPIView,CrearInstructorCreateAPIView,InstructoresRetriveAPIView

urlpatterns=[
    path("loggin/",Inicio_sesion.as_view()),
    path("instructores/",InstructoresListAPIView.as_view()),
    path("update/instructor/<int:id>/",NombreInstructor.as_view()),
    path("eliminarInstructor/<int:pk>/",InstructorDestroy.as_view()),
    path("busqueda/instructores/",BuscadorInstructor.as_view()),
    path("instructor/crear/",CrearInstructorCreateAPIView.as_view()),
    path("instructor/<int:pk>/",InstructoresRetriveAPIView.as_view()),
    path("instructoresdisponibles/",instructoresDisponiblesFecha),
    path("logout/",salir)
]