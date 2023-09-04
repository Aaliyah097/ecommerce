from haystack import indexes
from catalog.models import Products


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/indexes/product_text.txt')
    name = indexes.CharField(model_attr='name')
    name_auto = indexes.EdgeNgramField(model_attr='name')
    part_number = indexes.CharField(model_attr='part_number')
    brand = indexes.CharField(model_attr='brand__name')
    category = indexes.CharField(model_attr='category__name')
    specs = indexes.MultiValueField()

    def get_model(self):
        return Products

    def prepare_specs(self, obj):
        return [spec.value for spec in obj.specs.all()]

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all().select_related('brand', 'category').prefetch_related('specs', 'images')
