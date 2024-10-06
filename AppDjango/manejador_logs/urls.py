from django.urls import path
from .views import listar_logs

urlpatterns = [
    path('', listar_logs, name='listar_logs'),
]
