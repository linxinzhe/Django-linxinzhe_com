from django.conf.urls import url

import vue.views

app_name = "vue"

urlpatterns = [
    url(r'^$', vue.views.index, name='index'),
]
