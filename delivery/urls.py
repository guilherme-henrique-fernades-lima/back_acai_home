"""
URL configuration for delivery project.

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from delivery.core.views import pedidos, motoristas, home 

router = DefaultRouter()

router.register(r'pedidos', pedidos.PedidosViewSet, basename='pedidos')
router.register(r'motoristas', motoristas.MotoristasViewSet, basename='motoristas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index, name="index"),
    path('', include('django.contrib.auth.urls')),
    path('integration/', include(router.urls)),
    path('integration/', include(('delivery.users.routers', 'users'), namespace='users-api')),
    path('integration/', include(('delivery.auth.routers', 'auth'), namespace='auth-api')),
]

