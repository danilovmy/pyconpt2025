from django.contrib import admin
from django.urls import path, include
from settings import swagger
from django.conf import settings
from django.conf.urls.static import static

handler404 = "api.views.handler404"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/docs/", swagger.SwaggerTemplateView.as_view()),
    path("schema.yaml", swagger.YamlComposeView.as_view()),
    path("yaml.yaml", swagger.YamlView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
