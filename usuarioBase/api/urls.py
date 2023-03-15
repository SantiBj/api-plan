from django.urls import path
from .instructorViews import instructoresDisponiblesFecha,InstructoresListAPIView,CrearInstructorCreateAPIView

urlpatterns=[
    path("instructores/",InstructoresListAPIView.as_view()),
    path("instructor/crear/",CrearInstructorCreateAPIView.as_view()),
    path("instructoresdisponibles/",instructoresDisponiblesFecha)
]