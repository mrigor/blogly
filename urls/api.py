from django.conf.urls.defaults import patterns

urlpatterns = patterns('api.views',
    (r'^blog/(?P<blog_id>\d+)/$', 'blog'),
)
