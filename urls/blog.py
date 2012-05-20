from django.conf.urls.defaults import patterns, url

# Catch blog slugs
urlpatterns = patterns('blog.views',
    url(r'^$', 'blogs', name='blogs'),
    url(r'^save/$', 'blog_save', name='blog_save'),
    url(r'^(?P<slug>[-\w]+)/save/$', 'blog_save', name='blog_save'),
    url(r'^(?P<slug>[-\w]+)/$', 'blog', name='blog'),
)
