from django.urls import path
from .views import generar_reporte, home

urlpatterns = [
    path('', generar_reporte, name='generar_reporte'),
    path('', home, name='home'),  
    path('reporte/<str:nombre_institucion>/<str:mes>/', generar_reporte, name='generar_reporte'),
]
