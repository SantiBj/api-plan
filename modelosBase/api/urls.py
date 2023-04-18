from django.urls import path
from .views.tituladaViews import TituladaListAPIView
from .views.competenciaView import BuscadorCompetencias,CompetenciasTituladaListAPIView, anadirInstructorACompetencia,CompetenciasList
from .views.fichaViews import FichaDestroy, FichasTituladaListAPIView, FichaCreateAPIView, FichaTituladaBuscador, FichasListAPIView, FichaBuscador, FichaRetrieve
from .views.rapViews import RapSinAsignarDeCompetenciaListAPIView

urlpatterns = [
    path("programa/", TituladaListAPIView.as_view()),
    path("buscador/competencias/",BuscadorCompetencias.as_view()),
    path("competencias/",CompetenciasList.as_view()),
    path("competencias/programa/<int:pk>/",
         CompetenciasTituladaListAPIView.as_view()),
    path("fichasprograma/<int:pk>/", FichasTituladaListAPIView.as_view()),
    path("ficha/crear/", FichaCreateAPIView.as_view()),
    path("raps/competencia/<int:pkCompetencia>/<int:numeroficha>/",
         RapSinAsignarDeCompetenciaListAPIView.as_view()),
    path("anadirinstructor/", anadirInstructorACompetencia),
    path("ficha-buscador/", FichaTituladaBuscador.as_view()),
    path("fichaSearch/", FichaBuscador.as_view()),
    path("fichas/", FichasListAPIView.as_view()),
    path("ficha/<int:numero>/", FichaRetrieve.as_view()),
    path("fichaDelete/<int:pk>/", FichaDestroy.as_view())
]
