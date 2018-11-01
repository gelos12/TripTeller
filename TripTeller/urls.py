"""TripTeller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from accounts import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter

m_routsers = DefaultRouter()
m_routsers.register(r'user/signup', views.UserViewSet, base_name='signup')

schema_view = get_swagger_view(title='TripTeller API')

urlpatterns = [
    path('',schema_view),
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/', include('tourist.urls')),
    path('api/', include(m_routsers.urls)),
    path('api/user/', views.UserListAPIView.as_view(), name="user"),
    path('api/user/ranking/', views.UserRankingListAPIView.as_view(), name="ranking")
    
]

#디버그 모드일때 미디어파일 경로
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)