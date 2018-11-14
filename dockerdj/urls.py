"""dockerdj URL Configuration

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
from django.conf.urls import include, url
from django.urls import path
from . import views

from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path("dockerapp/",include("dockerapp.urls", namespace="dockerapp")),
    path("dockerapp/",include("django.contrib.auth.urls")),
    path("login_red/", views.LoginRedPage.as_view(), name="login_red"),
    path("logout_red/", views.LogoutRedPage.as_view(), name="logout_red"),
    url(r"^media/(?P<path>.*)$",serve,{'document_root':settings.MEDIA_ROOT}),
]
