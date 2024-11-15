from django.urls import path
from .views import listar_tareas

urlpatterns = [
    path('', listar_tareas, name='listar_tareas'),
]
