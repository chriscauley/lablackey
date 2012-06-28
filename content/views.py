from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseServerError)
from django.template import RequestContext
from django.shortcuts import render_to_response

from event.models import Event


def monitoring_test(request):
    # Never cache this view.
    Event.objects.order_by()[0]
    return HttpResponse('<html><body>working</body></html>')


def always_500_error(request):
    """Useful for testing no-ip.com monitoring failover."""
    return HttpResponseServerError('Monitoring test page. Always fail.')


def always_403_forbidden(request):
    """Useful for testing no-ip.com monitoring failover."""
    return HttpResponseForbidden('Monitoring test page. Always forbidden.')


def gps_redirect(request):
    return render_to_response(
        'content/gps_redirect.html',
        dict(),
        context_instance=RequestContext(request))
