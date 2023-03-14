from django.urls import path
from .views import asignacionesInstructorListAPIView,asignacionesFichaListAPIView,CrearAsignacionCreateAPIView
from .views import fechasAsignadasFicha

urlpatterns = [
    path("asignaciones/instructor/<int:pkInstructor>/",asignacionesInstructorListAPIView.as_view()),
    path("asignaciones/ficha/<int:pkFicha>/",asignacionesFichaListAPIView.as_view()),
    path("fechas-ocupadas-ficha/<int:pkFicha>/",fechasAsignadasFicha),
    path("crear/asignacion/",CrearAsignacionCreateAPIView.as_view())
]
