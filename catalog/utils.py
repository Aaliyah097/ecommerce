import django.db.models
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter


def get_router(name: str, view) -> list:
    r = SimpleRouter()
    r.register(name, view)
    return r.urls


class FormViewMixin:
    queryset: django.db.models.QuerySet = None
    template_name = 'form.html'
    serializer_class = None

    @action(renderer_classes=[renderers.TemplateHTMLRenderer], detail=False, url_path='form')
    def form_create(self, request):
        return Response(self.get_context())

    @action(renderer_classes=[renderers.TemplateHTMLRenderer], detail=True, url_path='form')
    def form_edit(self, request, pk):
        return Response(self.get_context(pk))

    def get_context(self, pk=None) -> dict:
        if pk:
            model = self.queryset.get(pk=pk)
            serializer = self.serializer_class(model)
        else:
            serializer = self.serializer_class()

        return {
            'form': serializer,
        }


