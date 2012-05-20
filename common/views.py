from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect, HttpResponseNotFound

def home(request):
    return HttpResponseRedirect(reverse('blog.views.blogs'))
