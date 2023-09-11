"""
URL configuration for L7 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import uploadFile,loadFile,vueLoader,webmethod,benfordPlot
urlpatterns = [
	path(r'', loadFile),
	path(r'files/<path:fileName>', loadFile),
	path(r'component/<str:componentName>', vueLoader),
	path(r'webmethod/<str:component>/<str:func>', webmethod),
	path(r'upload', uploadFile),
	path(r'plot/<str:fid>', benfordPlot),
]
