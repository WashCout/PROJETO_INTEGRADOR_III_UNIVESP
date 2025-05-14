from django.urls import path
from . import views

urlpatterns = [
    path('minhas-recomendacoes/', views.minhas_recomendacoes, name='minhas_recomendacoes'),

]
