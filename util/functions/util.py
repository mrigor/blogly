from random import randint

from django.core.urlresolvers import reverse

def url(view_name, *args, **kwargs):
    return reverse(view_name, args=args, kwargs=kwargs)

def rand():
    return unicode(randint(0, 2 ** 31 - 1))
