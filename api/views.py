from django.http import Http404, HttpResponse
from django.utils import simplejson

from blog.models import Blog
from common import render_to_remote_response

'''
Consider using Piston for this later
https://bitbucket.org/jespern/django-piston/wiki/Home
'''

def blog(request, blog_id=None):
    blog = None
    response = {}
    if blog_id:
        blog = Blog.objects.get(id=blog_id)
        if blog:
            fields =['name', 'description']
            for f in fields:
                response[f] = getattr(blog, f)
            #response = serializers.serialize("json", blog, fields=('name', 'description'))

    return HttpResponse(simplejson.dumps(response), mimetype='application/text')
