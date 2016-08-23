from django.conf.urls import url

import crawler.views

app_name = "crawler"

urlpatterns = [
    url(r'^$', crawler.views.index, name='index'),
    url(r'^crawl_gif/$', crawler.views.crawl_gif, name='crawl_gif'),
]
