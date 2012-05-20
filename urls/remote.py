from django.conf.urls.defaults import patterns

urlpatterns = patterns('remote.views',
    (r'^(?P<type>\w+)/comment/(?P<parent_id>\d+)/reply/$', 'comment_reply'),
    (r'^(?P<type>\w+)/comment/(?P<comment_id>\d+)/edit/$', 'comment_edit'),
)
