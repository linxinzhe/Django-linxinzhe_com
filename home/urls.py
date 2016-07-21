# -*- coding: utf-8 -*-
# __author__ = 'linxinzhe'
from django.conf.urls import url,include
import home.views

urlpatterns = [
    url(r'^$', home.views.index),
]