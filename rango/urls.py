from django.conf.urls import url

import rango.views

urlpatterns = [
    url(r'^$', rango.views.index, name='index'),
    url(r'^about/$', rango.views.about, name='about'),
]
