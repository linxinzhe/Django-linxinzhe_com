from django.conf.urls import url

import lab.views

app_name = "lab"

urlpatterns = [
    url(r'^$', lab.views.index, name='index'),
]
