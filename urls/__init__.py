from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.views import static
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    (r'^',                          include('urls.common')),
    (r'^accounts/',                 include('urls.accounts')),
    (r'^blog/',                     include('urls.blog')),
    (r'^profile/',                  include('urls.profiles')),
    (r'^remote/',                   include('urls.remote')),
    (r'^api/',                      include('urls.api')),
    (r'^static/(?P<path>.*)$',      static.serve, {'document_root': settings.MEDIA_ROOT}),
)
