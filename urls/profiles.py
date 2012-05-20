from django.conf.urls.defaults import patterns

urlpatterns = patterns('profiles.views',
    (r'^(?P<user_id>\d+)/$',    'profile'),
    (r'^save/(?P<user_id>\d+)/$',    'profile_save'),
)
