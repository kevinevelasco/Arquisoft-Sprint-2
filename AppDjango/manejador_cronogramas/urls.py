from django.urls import path
from .views import listar_cronogramas

urlpatterns = [
    path('', listar_cronogramas, name='listar_cronogramas'),
]
