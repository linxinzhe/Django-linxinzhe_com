from django.conf.urls import url

import rango.views

app_name = "rango"
urlpatterns = [
    url(r'^$', rango.views.index, name='index'),
    url(r'^about/$', rango.views.about, name='about'),
]
