"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.settings import DEBUG

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/admin/', admin.site.urls),
    path('api/token/', include('jwt_auth.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/developer/auth/', include('developer_auth.urls')),
    path('api/developer/profiles/', include('developer_profile.urls')),
    path('api/dicom/read/', include('dicom_reader.urls')),
    path('api/dicom/write/', include('dicom_writer.urls')),
    path('api/dicom-format/', include('dicom_format.urls'))
]

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += staticfiles_urlpatterns()
