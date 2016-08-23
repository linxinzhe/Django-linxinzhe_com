"""linxinzhe_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import registration.backends.simple.urls
from django.conf.urls import url, include
from django.contrib import admin

import home.urls
import lab.urls
import rango.urls
import vue.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(home.urls)),
    url(r'^rango/', include(rango.urls)),
    url(r'^lab/', include(lab.urls)),
    url(r'^vue/', include(vue.urls)),
    url(r'^accounts/', include(registration.backends.simple.urls)),
    url(r'^accounts/register/$', rango.views.MyRegistrationView.as_view(), name="registration_register"),
]
