from django.http import HttpResponse, JsonResponse
from django.views.defaults  import page_not_found
from django.views import debug
# Create your views here.







def index(*args, **kwargs):
    return HttpResponse('Hello World!')

def handler404(request, exception, *args, **kwargs):
    if request.content_type == 'application/json':
        return JsonResponse({'message': 'Not Found'}, status=404)
    return page_not_found(request, exception, *args, **kwargs)  # default 404


def handler500(request, handler=debug.technical_404_response):
    if request.content_type == 'application/json':
        return JsonResponse({'message': 'Server Error'}, status=404)
    return HttpResponse('500')

def tech_404(request, exception, handler=debug.technical_404_response):
    if "/api/" in request.path:
        return handler404(request, exception)
    return handler(request, exception)

debug.technical_404_response = tech_404
