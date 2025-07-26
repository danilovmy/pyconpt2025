
from .views import index, PetDetailView
from django.urls import path
from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    path('schema.yaml', RedirectView.as_view(url='/media/schema.yaml'), name='schema.yaml'),
    path('docs/', TemplateView.as_view(template_name='schema.html'), name='docs'),
    path('pet/<int:petid>', PetDetailView.as_view(), name='pet-detail'),
    path('', index, name='index'),
]
