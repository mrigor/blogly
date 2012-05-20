from django.conf.urls.defaults import patterns, url

# Standard common urls
urlpatterns = patterns('common.views',
    (r'^$', 'home'),
)
