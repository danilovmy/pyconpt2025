from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView
from django.views.defaults import page_not_found
from django.views import debug


class MyJsonResponse(JsonResponse):
    def __init__(self, request=None, template=None, context=None, using=None, **response_kwargs):
        super().__init__(context, **response_kwargs)

class MyHttpResponse(HttpResponse):
    def __init__(self, request=None, template=None, context=None, using=None, **response_kwargs):
        super().__init__(content=context, **response_kwargs)


# Create your views here.
class APIViewMixIn(DetailView):
    """
            requestBody:
                description: Information about a new pet in the system
                content:
                application/json:
                    schema:
                    Pet:
                    required:
                        - id
                        - name
                    properties:
                        id:
                        type: integer
                        format: int64
                        name:
                        type: string
                        tag:
                        type: string
            responses:
                "200":
                description
"""
    response_class = JsonResponse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def options(self, request, *args, **kwargs):

        response = super().options(request, *args, **kwargs)
        if 'yaml' in self.request.headers.get('Content-Type', ''):
            response.headers['Content-Disposition'] = 'attachment; filename="schema.yaml"'
            response.headers['Content-Type'] = self.request.headers['Content-Type']
            response.headers.pop("Content-Length", None)
            response.content = type(self).__doc__
        return response

def handler404(request, exception):
    if '/api/' in request.path:
        return MyJsonResponse(context={'message': 'Not found', 'error': f'{exception}'}, status=404)
    return page_not_found(request, exception)

def tech_404(request, exception, handler=debug.technical_404_response):
    if '/api/' in request.path:
        return MyJsonResponse(context={'message': 'Not found', 'error': f'{exception}'}, status=404)
    return handler(request, exception)

debug.technical_404_response = tech_404