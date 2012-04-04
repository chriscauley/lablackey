from django import template
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from content.models import Page, Copy, DesignImage, ItemList
from asset.models import DigitalAsset

@user_passes_test(lambda u: u.is_staff)
def fauxadmin(request):
    """
    Content model modified admin front end.
    Currently the variables are very poorly named.
    This is because I am using the admin template.
    This is ripping off django.contrib.admin.sites.index
    """
    pages = Page.objects.all()
    models = [o.model for o in Page._meta.get_all_related_objects()]
    perms = lambda m: {
        'add': request.user.is_superuser,
        'change': request.user.is_staff }
    app_list = [{
            'name': 'Auth',
            'app_url': '/admin/auth/',
            'models': [
                {'name': 'Users',
                 'admin_url': '/admin/auth/user/',
                 'perms': {'add': True,'change': True},
                 },
                ]}]
    if not 'auth.add_user' in request.user.get_all_permissions():
        app_list = []
    for p in pages:
        app = { 'name': p.name.title(), 'models': [], 'app_url': "/%s"%p.name }

        for m in models:
            if getattr(p,m.__name__.lower()+'_set').count():
                tup = (m._meta.app_label,m.__name__.lower(),p.id)
                admin_url = '/admin/%s/%s/?page__id__exact=%s'%tup
                app['models'].append(
                    {'admin_url': admin_url,
                     'name': getattr(m._meta,'verbose_name_plural',m.__name__),
                     'perms': perms(m)
                     })
        app_list.append(app)
    context = {
        'title': _('Site administration'),
        'app_list': app_list,
        'root_path': '/admin/', #this is 'self.root_path' in the model I copied...
        }
    # context.update(extra_context or {})
    context_instance = template.RequestContext(request) #why was this here?: , current_app=self.name)
    return render_to_response('admin/index.html', context, # template could be self.index_template instead
                              context_instance=context_instance
                              )
