from django.urls import path
from .instructorViews import InstructorDestroy,BuscadorInstructor,salir,instructoresDisponiblesFecha,InstructoresListAPIView,CrearInstructorCreateAPIView,InstructoresRetriveAPIView

urlpatterns=[
    path("instructores/",InstructoresListAPIView.as_view()),
    path("eliminarInstructor/<int:pk>/",InstructorDestroy.as_view()),
    path("busqueda/instructores/",BuscadorInstructor.as_view()),
    path("instructor/crear/",CrearInstructorCreateAPIView.as_view()),
    path("instructor/<int:pk>/",InstructoresRetriveAPIView.as_view()),
    path("instructoresdisponibles/",instructoresDisponiblesFecha),
    path("salir/",salir)
]