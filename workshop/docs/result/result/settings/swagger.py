from django.views.generic import TemplateView, RedirectView, View
from django.conf import settings
import yaml
from deepmerge import always_merger


class SwaggerTemplateView(TemplateView):
    template_name = "swagger.html"


class YamlView(RedirectView):
    url = settings.MEDIA_URL + "schema.yaml"


class YamlComposeView(View):

    def collect_yaml(self, *args, **kwargs):
        for method in self._allowed_methods():
            handler = getattr(self, method.lower(), None)
            if handler.__doc__:
                yield yaml.load(handler.__doc__, yaml.Loader)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        if "yaml" in self.request.headers.get("Content-Type", ""):
            response.headers["Content-Disposition"] = (
                'attachment; filename="schema.yaml"'
            )
            response.headers["Content-Type"] = self.request.headers["Content-Type"]
            response.headers.pop("Content-Length", None)
            schemas = self.collect_yaml()
            schema = next(schemas)
            for next_schema in schemas:
                schema = always_merger.merge(schema, next_schema)
            response.content = yaml.dump(schema)
        return response

    def get(self, request, *args, **kwargs):
        """
        openapi: "3.0.0"
        info:
          version: 1.0.0
          title: Swagger Petstore
          license:
            name: MIT
        servers:
          - url: http://localhost:8000/api
        paths:
          /pets:
            get:
              summary: List all pets
              operationId: listPets
              tags:
                - pets
              parameters:
                - name: limit
                  in: query
                  description: How many items to return at one time (max 100)
                  required: false
                  schema:
                    type: integer
                    maximum: 100
                    format: int32
              responses:
                '200':
                  description: A paged array of pets
                  headers:
                    x-next:
                      description: A link to the next page of responses
                      schema:
                        type: string
                  content:
                    application/json:
                      schema:
                        $ref: "#/components/schemas/Pets"
                default:
                  description: unexpected error
                  content:
                    application/json:
                      schema:
                        $ref: "#/components/schemas/Error"
        components:
          schemas:
            Pet:
              type: object
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
            Pets:
              type: array
              maxItems: 100
              items:
                $ref: "#/components/schemas/Pet"
            Error:
              type: object
              required:
                - code
                - message
              properties:
                code:
                  type: integer
                  format: int32
                message:
                  type: string
        """
        self.request.headers = dict(self.request.headers, **{"Content-Type": "yaml"})
        return self.options(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        openapi: "3.0.0"
        info:
          version: 1.0.0
          title: Swagger Petstore
          license:
            name: MIT
        servers:
          - url: http://localhost:8000/api
        paths:
          /pets:
            post:
              summary: Create a pet
              operationId: createPets
              tags:
                - pets
              requestBody:
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/Pet'
                required: true
              responses:
                '201':
                  description: Null response
                default:
                  description: unexpected error
                  content:
                    application/json:
                      schema:
                        $ref: "#/components/schemas/Error"
        components:
          schemas:
            Pet:
              type: object
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
            Pets:
              type: array
              maxItems: 100
              items:
                $ref: "#/components/schemas/Pet"
            Error:
              type: object
              required:
                - code
                - message
              properties:
                code:
                  type: integer
                  format: int32
                message:
                  type: string
        """
        self.request.headers = dict(self.request.headers, **{"Content-Type": "yaml"})
        return self.options(request, *args, **kwargs)
