from django.urls import path, include
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.index, name='index'),
    path('exams', views.exams, name='exams'),
    path('results', views.results, name='results'),
]
