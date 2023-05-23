from django.urls import path
from .views import AsignacionesActivasInstructor,DeleteAsignacion,AsignacionesActivasFichas,ReportFicha,Report,asignacionesInstructorListAPIView,asignacionesFichaListAPIView,CrearAsignacionCreateAPIView
from .views import fechasAsignadasFicha

urlpatterns = [
    path("reporteFicha/",ReportFicha.as_view()),
    path("reporte/",Report.as_view()),
    path("delete/asignacion/<int:pk>/",DeleteAsignacion.as_view()),
    path("asignaciones/activas/inst/<int:doc>/",AsignacionesActivasInstructor.as_view()),
    path("asignaciones/activas/<int:ficha>/",AsignacionesActivasFichas.as_view()),
    path("asignaciones/instructor/<int:pkInstructor>/",asignacionesInstructorListAPIView.as_view()),
    path("asignaciones/ficha/<int:pkFicha>/",asignacionesFichaListAPIView.as_view()),
    path("fechas-ocupadas-ficha/<int:pkFicha>/",fechasAsignadasFicha),
    path("crear/asignacion/",CrearAsignacionCreateAPIView.as_view())
]
