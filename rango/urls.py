from django.conf.urls import url

import rango.views

app_name = "rango"

urlpatterns = [
    url(r'^$', rango.views.index, name='index'),
    url(r'^about/$', rango.views.about, name='about'),
    url(r'^add_category/$', rango.views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', rango.views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', rango.views.add_page, name='add_page'),
    # url(r'^register/$', rango.views.register, name='register'),
    # url(r'^login/$', rango.views.user_login, name='login'),
    # url(r'^logout/$', rango.views.user_logout, name='logout'),
    url(r'search/$', rango.views.search, name='search'),
    url(r'^goto/$', rango.views.track_url, name='goto'),
    url(r'^add_profile/$', rango.views.register_profile, name='add_profile'),
    url(r'^profile/$', rango.views.profile, name='profile'),
]
