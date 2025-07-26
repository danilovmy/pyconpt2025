
from .views import SwaggerTemplateView, PetDetailView
from django.urls import path


urlpatterns = [
    path('docs/', SwaggerTemplateView.as_view()),
    path('pet/<int:petid>', PetDetailView.as_view()),

]