from lablackey.photo.models import Photo


class PhotoLookup(object):

    def get_query(self, q, request):
        """Return a query set."""
        # Filter by search string.
        return Photo.objects.filter(name__icontains=q)

    def format_result(self, photo):
        """The search results display in the dropdown menu.

        may contain html and multiple-lines. will remove any '|'.
        """
        # thumbnail_link_128x128 is actually only necessary for
        # format_item(), since format_result() is used for the dropdown
        # menu, and clicking on a menu item will not trigger the <a>
        # click handler. However, this allows format_item() and
        # format_result() to be the same for easy updating.
        return u'%s<br/>%s' % (
            unicode(photo), photo.thumbnail_link_128x128)

    def format_item(self, photo):
        """Currently selected object in the area below the search box.

        HTML is OK.
        """
        return self.format_result(photo)

    def get_objects(self, ids):
        """Order currently selected items (for a ManyToMany field)."""
        return Photo.objects.filter(pk__in=ids).order_by('name')
