import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    logger.debug('Something debug!')
    logger.info('Something info!')
    logger.warning('Something warning!')
    logger.error('Something error!')
    logger.critical('Something critical!')
    return render(request, "home/index.html")
