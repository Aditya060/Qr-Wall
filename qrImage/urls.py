"""
URL configuration for qrImage project.

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
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.large_screen, name='large_screen'),
    path('reveal/<str:segment>/', views.reveal, name='reveal'),
    path('success/', views.success_page, name='success_page'),
    path('qr_code_status/', views.qr_code_status, name='qr_code_status'),
    path('reset/', views.reset_revealed_segments, name='reset_revealed_segments'), 

   

]


