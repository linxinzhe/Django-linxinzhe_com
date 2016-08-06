import datetime
import time

from django.shortcuts import render
from django.utils import timezone


# Create your views here.
def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    b = datetime.datetime.utcfromtimestamp(time.time())
    a = timezone.now()
    c = timezone.now() + datetime.timedelta(days=1)
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)
