from django.db.models import Prefetch
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from catalog.models import Products, Brands, Categories, Specs


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'product'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    # brand = fields.ObjectField(properties={
    #     'name': fields.TextField(),
    # })
    #
    # category = fields.ObjectField(properties={
    #     'name': fields.TextField()
    # })
    #
    # specs = fields.ObjectField(properties={
    #     'detail': fields.ObjectField(properties={
    #         'name': fields.TextField()
    #     }),
    #     'value': fields.TextField()
    # })

    part_number = fields.KeywordField()
    # name = fields.TextField()

    class Django:
        model = Products

        # related_models = [Brands, Categories]

    # def get_queryset(self):
    #     return super(ProductDocument, self).get_queryset().select_related('brand', 'category').prefetch_related(
    #         Prefetch(
    #             'specs',
    #             Specs.objects.all().select_related('detail')
    #         )
    #     )

    # @staticmethod
    # def get_instances_from_related(related_instance):
    #     if isinstance(related_instance, Brands):
    #         return related_instance.products_by_brand.all()
    #     elif isinstance(related_instance, Categories):
    #         return related_instance.products_by_category.all()
