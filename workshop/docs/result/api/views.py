from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import Serializer
from django.shortcuts import aget_object_or_404
from django.views import debug
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import BaseDetailView

from django.views.defaults import page_not_found
from django.forms.models import model_to_dict

from pets.models import Pet
# Create your views here.

class MyJsonResponse(JsonResponse):
    def __init__(self, request=None, template=None, context=None, using=None, **response_kwargs):
        super().__init__(context, **response_kwargs)



class PetDetailView(DetailView):
    response_class = MyJsonResponse
    model = Pet
    pk_url_kwarg = 'petid'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        return model_to_dict(context['object'])
    
    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        if 'yaml' in self.request.headers.get('Content-Type', ''):
            response.headers['Content-Disposition'] = 'attachment; filename="schema.yaml"'
            response.headers['Content-Type'] = self.request.headers['Content-Type']
            response.headers.pop("Content-Length", None)
            response.content = type(self).__doc__
        return response


class BasePetDetailView(BaseDetailView):
    model = Pet
    pk_url_kwarg = 'petid'

    def render_to_response(self, *args, **kwargs):
        data = Serializer().serialize([self.object], **kwargs)
        return HttpResponse(data, content_type="application/json")


class AsyncPetDetailView(BaseDetailView):
    model = Pet
    pk_url_kwarg = 'petid'
    response_class = MyJsonResponse

    async def get(self, request, *args, **kwargs):
        self.object = await self.get_object()
        return self.render_to_response()

    def render_to_response(self, *args, **kwargs):
        data = Serializer().serialize([self.object], fields=self.request.GET.get('fields'), **kwargs)
        return HttpResponse(data, content_type="application/json")

    async def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return await aget_object_or_404(self.model, pk=pk)











class SwaggerTemplateView(TemplateView):
    template_name = 'swagger.html'


def handler404(request, exception):
    if '/api/' in request.path:
        return MyJsonResponse(context={'message': 'Not found', 'error': f'{exception}'}, status=404)# some json
    return page_not_found(request, exception) # default 404


def tech_404(request, exception, handler=debug.technical_404_response):
    if '/api/' in request.path:
        return MyJsonResponse(context={'message': 'Not found', 'error': f'{exception}'}, status=404)
    return handler(request, exception)

debug.technical_404_response = tech_404
