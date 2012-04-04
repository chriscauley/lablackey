from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Article, Tag
from lablackey.photo.admin_mixins import PhotoManyToManyForm

class ArticleAdminForm(PhotoManyToManyForm):
    tags = forms.CharField(initial='', required=False,
                           widget=forms.TextInput(attrs={'size': 100}),
                           help_text=_('Words that describe this article'))

    def __init__(self, *args, **kwargs):
        """Sets the list of tags to be a string"""

        instance = kwargs.get('instance', None)
        if instance:
            init = kwargs.get('initial', {})
            init['tags'] = ' '.join([t.name for t in instance.tags.all()])
            kwargs['initial'] = init

        super(ArticleAdminForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        """Turns the string of tags into a list"""

        tag = lambda n: Tag.objects.get_or_create(name=Tag.clean_tag(n))[0]
        tags = [tag(t) for t in self.cleaned_data['tags'].split()]
        self.cleaned_data['tags'] = tags
        return self.cleaned_data['tags']

    class Meta:
        model = Article

    class Media:
        css = {
            'all': (
                'articles_media/css/jquery.autocomplete.css',
                'ajax_select/iconic.css',
                ),
        }
        js = (
            # Fix IE6 z-index issue with <select>.
            'articles_media/js/jquery.bgiframe.min.js',
            # For autocomplete.
            'jquery/jquery-1.5.min.js',
            'jquery/jquery.autocomplete.js',
            # Photo autocomplete.
            'ajax_select/ajax_select.js',
            # Tag autocomplete.
            'articles_media/js/tag_autocomplete.js',
        )

