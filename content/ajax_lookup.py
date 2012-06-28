from guide.models import Place


class PlaceLookup(object):

    def get_query(self, q, request):
        """Return a query set."""
        # Filter by search string.
        queryset = Place.objects.filter(name__icontains=q)
        return queryset

    def format_result(self, place):
        """The search results display in the dropdown menu.

        may contain html and multiple-lines. will remove any '|'.
        """
        return unicode(place)

    def format_item(self, place):
        """Currently selected object in the area below the search box.

        HTML is OK.
        """
        return unicode(place)

    def get_objects(self, ids):
        """Order currently selected items (for a ManyToMany field)."""
        return Place.objects.filter(pk__in=ids).order_by('name')
