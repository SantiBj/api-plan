from django.urls import path
from .views.programaViews import ProgramaListAPIView,ProgramaCreateAPIView

urlpatterns = [
    path("programa/",ProgramaListAPIView.as_view()),
    path("programa/crear",ProgramaCreateAPIView.as_view())
]