from django.conf.urls.defaults import patterns

# Standard common urls
urlpatterns = patterns('accounts.views',
    (r'^register/$',          'register'),
    (r'^login/$',             'login'),
    (r'^logout/$',            'logout'),
)
