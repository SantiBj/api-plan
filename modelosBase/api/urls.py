from django.urls import path
from .views.programaViews import ProgramaListAPIView
from .views.competenciaView import CompetenciasProgramaListAPIView
from .views.fichaViews import FichasProgramaListAPIView,FichaCreateAPIView
from .views.rapViews import RapSinAsignarDeCompetenciaListAPIView

urlpatterns = [
    path("programa/",ProgramaListAPIView.as_view()),
    path("competencias/programa/<int:pkPrograma>/",CompetenciasProgramaListAPIView.as_view()),
    path("fichasprograma/<int:pk>/",FichasProgramaListAPIView.as_view()),
    path("ficha/crear/",FichaCreateAPIView.as_view()),
    path("raps/competencia/<int:pkCompetencia>/<int:numeroficha>",RapSinAsignarDeCompetenciaListAPIView.as_view())
]