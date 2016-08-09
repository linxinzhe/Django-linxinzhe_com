from django.conf.urls import url

import rango.views

app_name = "rango"

urlpatterns = [
    url(r'^$', rango.views.index, name='index'),
    url(r'^about/$', rango.views.about, name='about'),
    url(r'^add_category/$', rango.views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', rango.views.show_category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', rango.views.add_page, name='add_page'),
]
