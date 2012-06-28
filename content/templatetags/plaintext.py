from BeautifulSoup import BeautifulSoup as Soup
from django import template

register = template.Library()


@register.filter
def plaintext(text):
    # Convert HTML entities to ascii or unicode characters.
    soup = Soup(text, convertEntities=Soup.HTML_ENTITIES)
    # Remove the style tags and their content.
    for style in soup.findAll('style'):
        style.replaceWith('')
    # Remove the script tags and their content.
    for style in soup.findAll('script'):
        style.replaceWith('')
    return (''.join(soup.findAll(text=True))).strip()
