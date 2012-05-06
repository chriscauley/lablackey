import datetime
from haystack.indexes import *
from haystack import site
from articles.models import Article

class ArticleIndex(SearchIndex):
  content = CharField(document=True, use_template=True)
  author = CharField(model_attr='author')
  publish_date = DateTimeField(model_attr='publish_date')

  def get_model(self):
    return Article

  def index_queryset(self):
    """Used when the entire index for model is updated."""
    return self.get_model().objects.filter(publish_date__lte=datetime.datetime.now())

site.register(Article,ArticleIndex)
