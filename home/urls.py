# -*- coding: utf-8 -*-
# __author__ = 'linxinzhe'
from django.conf.urls import url

import home.views

app_name = "home"
urlpatterns = [
    url(r'^$', home.views.index),
]
