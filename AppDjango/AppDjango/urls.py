"""
URL configuration for AppDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manejador_cronogramas/', include('manejador_cronogramas.urls')),
    path('manejador_facturacion/', include('manejador_facturacion.urls')),
    path('manejador_batch_processing/', include('manejador_batch_processing.urls')),
    path('manejador_reportes/', include('manejador_reportes.urls')),
    path('manejador_logs/', include('manejador_logs.urls')),
    path('', RedirectView.as_view(url='/admin/', permanent=False))
]

