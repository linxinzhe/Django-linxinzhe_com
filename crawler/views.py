import requests
from bs4 import BeautifulSoup
from django.core import serializers
from django.shortcuts import render, HttpResponse

from crawler.models import Gif


def index(request):
    return render(request, "crawler/index.html")


def crawl_gif(request):
    html = requests.get("http://qq.yh31.com/ka/qw/")
    html.encoding = "utf-8"
    html_text = html.text
    soup = BeautifulSoup(html_text, "html.parser")
    imgs = soup.select("li dt a img")
    for img in imgs:
        src = img["src"]
        src = "http://qq.yh31.com" + src
        alt = img["alt"]
        gif = Gif.objects.get_or_create(name=alt, url=src)
        gif[0].save()
    json = serializers.serialize("json", Gif.objects.all())
    return HttpResponse(json)
