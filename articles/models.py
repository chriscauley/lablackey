from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.markup.templatetags import markup
from django.core.cache import cache
from django.conf import settings
from django.template.defaultfilters import slugify, striptags
from django.utils.translation import ugettext_lazy as _
from django.utils.text import truncate_html_words
from datetime import datetime
from base64 import encodestring
import mimetypes
import re
import urllib
from lablackey.photo.models import Photo

WORD_LIMIT = getattr(settings, 'ARTICLES_TEASER_LIMIT', 50)
AUTO_TAG = getattr(settings, 'ARTICLES_AUTO_TAG', True)

MARKUP_HTML = 'h'
MARKUP_MARKDOWN = 'm'
MARKUP_REST = 'r'
MARKUP_TEXTILE = 't'
MARKUP_OPTIONS = getattr(settings, 'ARTICLE_MARKUP_OPTIONS', (
        (MARKUP_HTML, _('HTML/Plain Text')),
        (MARKUP_MARKDOWN, _('Markdown')),
        (MARKUP_REST, _('ReStructured Text')),
        (MARKUP_TEXTILE, _('Textile'))
    ))
MARKUP_DEFAULT = getattr(settings, 'ARTICLE_MARKUP_DEFAULT', MARKUP_HTML)

USE_ADDTHIS_BUTTON = getattr(settings, 'USE_ADDTHIS_BUTTON', True)
ADDTHIS_USE_AUTHOR = getattr(settings, 'ADDTHIS_USE_AUTHOR', True)
DEFAULT_ADDTHIS_USER = getattr(settings, 'DEFAULT_ADDTHIS_USER', None)

# regex used to find links in an article
LINK_RE = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>', re.I|re.M)
TITLE_RE = re.compile('<title>(.*?)</title>', re.I|re.M)
TAG_RE = re.compile('[^a-z0-9\-_\+\:\.]?', re.I)

def get_name(user):
    """
    Provides a way to fall back to a user's username if their full name has not
    been entered.
    """
    key = 'username_for_%s' % user.id
    name = cache.get(key)
    if not name:
        if len(user.get_full_name().strip()):
            name = user.get_full_name()
        else:
            name = user.username
        cache.set(key, name, 86400)

    return name
User.get_name = get_name

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def clean_tag(name):
        """Replace spaces with dashes, in case someone adds such a tag manually"""

        name = name.replace(' ', '-')
        name = TAG_RE.sub('', name)
        return name.lower().strip()

    def save(self, *args, **kwargs):
        """Cleans up any characters I don't want in a URL"""

        self.name = Tag.clean_tag(self.name)
        super(Tag, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('articles_display_tag', (self.name,))

    @property
    def rss_name(self):
        return u'tags/%s' % self.name

    class Meta:
        ordering = ('name',)

class ArticleManager(models.Manager):
    def live(self, user=None):
        """Retrieves all live articles"""
        return self.filter(is_live=True)

MARKUP_HELP = _("""Select the type of markup you are using in this article.
<ul>
<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>
<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>
</ul>""")

class Article(models.Model):
    class Meta:
        ordering = ('-publish_date', 'title')
        verbose_name = 'Post'

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique_for_year='publish_date')
    author = models.ForeignKey(User, limit_choices_to={'is_staff': True},default=0)

    description = models.TextField(blank=True, help_text=_("If omitted, the description will be determined by the first bit of the article's content."))
    markup = models.CharField(max_length=1, choices=MARKUP_OPTIONS,
                              default=MARKUP_DEFAULT, help_text=MARKUP_HELP)
    content = models.TextField()
    rendered_content = models.TextField()

    tags = models.ManyToManyField(Tag, help_text=_('Tags that describe this article'), blank=True)
    auto_tag = models.BooleanField(default=AUTO_TAG, blank=True, help_text=_('Check this if you want to automatically assign any existing tags to this article based on its content.'))
    followup_for = models.ManyToManyField('self', symmetrical=False, blank=True, help_text=_('Select any other articles that this article follows up on.'), related_name='followups')
    related_articles = models.ManyToManyField('self', blank=True)

    publish_date = models.DateTimeField(default=datetime.now, help_text=_('The date and time this article shall appear online.'))
    is_live = models.BooleanField(default=True, blank=True)
    images = models.ManyToManyField(Photo, blank=True)

    objects = ArticleManager()

    def summary(self): #for haystack search page
        from django.template.defaultfilters import striptags,truncatewords
        from django.utils.safestring import mark_safe
        return mark_safe(striptags(truncatewords(self.content,100)))
    summary.is_safe=True

    def __unicode__(self):
        return self.title

    @property
    def first_image(self):
        result = self.images.all()[:1]
        if len(result) == 0:
            return None
        else:
            return result[0]

    def save(self, *args, **kwargs):
        """Renders the article using the appropriate markup language."""
        using = kwargs.get('using', 'default')

        # If the rendered markup (i.e. content) has changed,
        # update the meta description.
        if self.do_render_markup():
            # The description has to be cleared, or the teaser will
            # return the description instead of generating a new one
            # from the content.
            self.description = ''
            self.description = self.teaser
        self.do_unique_slug(using)

        super(Article, self).save(*args, **kwargs)
        # do some things that require an ID first
        requires_save = self.do_auto_tag(using)

        if requires_save:
            # bypass the other processing
            super(Article, self).save()

    def do_render_markup(self):
        """Turns any markup into HTML"""
        original = self.rendered_content
        if self.markup == MARKUP_MARKDOWN:
            self.rendered_content = markup.markdown(self.content)
        elif self.markup == MARKUP_REST:
            self.rendered_content = markup.restructuredtext(self.content)
        elif self.markup == MARKUP_TEXTILE:
            self.rendered_content = markup.textile(self.content)
        else:
            self.rendered_content = self.content
        return (self.rendered_content != original)

    def do_unique_slug(self, using):
        """
        Ensures that the slug is always unique for the year this article was
        posted
        """
        if not self.id:
            # make sure we have a slug first
            if not len(self.slug.strip()):
                self.slug = slugify(self.title)

            self.slug = self.get_unique_slug(self.slug, using)
            return True

        return False

    def do_auto_tag(self, using='default'):
        """
        Performs the auto-tagging work if necessary.
        Returns True if an additional save is required, False otherwise.
        """
        found = False
        if self.auto_tag:
            # don't clobber any existing tags!
            existing_ids = [t.id for t in self.tags.all()]
            unused = Tag.objects.using(using).exclude(id__in=existing_ids)
            for tag in unused:
                regex = re.compile(r'\b%s\b' % tag.name, re.I)
                if regex.search(self.content) or regex.search(self.title) or \
                   regex.search(self.description):
                    self.tags.add(tag)
                    found = True

        return found

    def get_unique_slug(self, slug, using):
        """Iterates until a unique slug is found"""

        # we need a publish date before we can do anything meaningful
        if type(self.publish_date) is not datetime:
            return slug

        orig_slug = slug
        year = self.publish_date.year
        counter = 1

        while True:
            not_unique = Article.objects.using(using).filter(publish_date__year=year, slug=slug)
            if len(not_unique) == 0:
                return slug

            slug = '%s-%s' % (orig_slug, counter)
            counter += 1

    def _get_article_links(self):
        """
        Find all links in this article.  When a link is encountered in the
        article text, this will attempt to discover the title of the page it
        links to.  If there is a problem with the target page, or there is no
        title (ie it's an image or other binary file), the text of the link is
        used as the title.  Once a title is determined, it is cached for a week
        before it will be requested again.
        """
        links = {}
        keys = []

        # find all links in the article
        for link in LINK_RE.finditer(self.rendered_content):
            url = link.group(1)
            key = 'href_title_' + encodestring(url).strip()

            # look in the cache for the link target's title
            if not cache.get(key):
                try:
                    # open the URL
                    c = urllib.urlopen(url)
                    html = c.read()
                    c.close()

                    # try to determine the title of the target
                    title = TITLE_RE.search(html)
                    if title: title = title.group(1)
                    else: title = link.group(2)
                except:
                    # if anything goes wrong (ie IOError), use the link's text
                    title = link.group(2)

                # cache the page title for a week
                cache.set(key, title, 604800)

            # get the link target's title from cache
            val = cache.get(key)
            if val:
                # add it to the list of links and titles
                links[url] = val

                # don't duplicate links to the same page
                if url not in keys: keys.append(url)

        # now go thru and sort the links according to where they appear in the
        # article
        sorted = []
        for key in keys:
            sorted.append((key, links[key]))

        return tuple(sorted)
    links = property(_get_article_links)

    def _get_word_count(self):
        """Stupid word counter for an article."""

        return len(striptags(self.rendered_content).split(' '))
    word_count = property(_get_word_count)

    @models.permalink
    def get_absolute_url(self):
        return ('articles_display_article', (self.publish_date.year, self.slug))

    @property
    def teaser(self):
        """Retrieve some part of the article or the article's description."""
        if not getattr(self,'_teaser',False):
            if len(self.description.strip()):
                text = self.description
            else:
                text = self.rendered_content

            self._teaser = truncate_html_words(text, WORD_LIMIT)

        return self._teaser

    def get_next_article(self):
        """Determines the next live article"""

        if not getattr(self,'_next',False):
            try:
                qs = Article.objects.live().exclude(id__exact=self.id)
                article = qs.filter(publish_date__gte=self.publish_date).order_by('publish_date')[0]
            except (Article.DoesNotExist, IndexError):
                article = None
            self._next = article

        return self._next

    def get_previous_article(self):
        """Determines the previous live article"""

        if not getattr(self,'_previous',False):
            try:
                qs = Article.objects.live().exclude(id__exact=self.id)
                article = qs.filter(publish_date__lte=self.publish_date).order_by('-publish_date')[0]
            except (Article.DoesNotExist, IndexError):
                article = None
            self._previous = article

        return self._previous


class Attachment(models.Model):
    upload_to = lambda inst, fn: 'attach/%s/%s/%s' % (datetime.now().year, inst.article.slug, fn)

    article = models.ForeignKey(Article, related_name='attachments')
    attachment = models.FileField(upload_to=upload_to)
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ('-article', 'id')

    def __unicode__(self):
        return u'%s: %s' % (self.article, self.caption)

    @property
    def filename(self):
        return self.attachment.name.split('/')[-1]

    @property
    def content_type_class(self):
        mt = mimetypes.guess_type(self.attachment.path)[0]
        if mt:
            content_type = mt.replace('/', '_')
        else:
            # assume everything else is text/plain
            content_type = 'text_plain'

        return content_type

