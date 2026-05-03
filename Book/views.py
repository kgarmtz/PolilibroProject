import logging

from django.http import HttpResponseNotFound


logger = logging.getLogger(__name__)


def fake_admin(request):
    if request.method == 'POST':
        logger.warning('Fake admin login attempt from %s', request.META.get('REMOTE_ADDR'))
    return HttpResponseNotFound('Page Requested was not found')
