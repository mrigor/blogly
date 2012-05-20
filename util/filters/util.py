from __future__ import absolute_import

from datetime import datetime
import locale

from django.template.defaultfilters import \
    add as django_add, \
    date as django_date, \
    floatformat as django_floatformat, \
    linebreaks as django_linebreaks, \
    pluralize as django_pluralize, \
    safe as django_safe, \
    truncatewords as django_truncatewords, \
    urlizetrunc as django_urlizetrunc, \
    yesno as django_yesno
from django.contrib.markup.templatetags.markup import restructuredtext as django_restructuredtext

from jinja2 import Undefined
from jinja2.utils import Markup

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def add(value, num):
    return Markup(django_add(value, num))

def safe(value):
    return Markup(django_safe(value))

def floatformat(value, num=-1):
    if isinstance(value, Undefined):
        return ''
    return Markup(django_floatformat(value, num))

def linebreaks(value):
    return Markup(django_linebreaks(value))

def truncatewords(value, num):
    return Markup(django_truncatewords(value, num))

def yesno(value, text):
    return Markup(django_yesno(value, text))

def urlizetrunc(value, num):
    return Markup(django_urlizetrunc(value, num))

def pluralize(value, args=u's'):
    return Markup(django_pluralize(value, args))

def plural(value, singular='', plural='s'):
  if value is not None:
    if isinstance(value, (int, long)):
      return singular if value == 1 else plural
    return singular if len(value) == 1 else plural
  return ''

def restructuredtext(value):
    return Markup(django_restructuredtext(value))

def date(value, f='M/d/Y h:m a'):
    '''
    NNN. d, yyyy
    '''
    return Markup(django_date(value, f))

def datedelta(date, short=False):
  """
  Filter to create display string representing the delta from now to the given
  date.
  """
  if not date:
      return ''

  from dateutil.relativedelta import relativedelta
  delta = relativedelta(datetime.now(), date)
  if delta.years > 0:
      return '%i year%s ago' % (delta.years, plural(delta.months))
  if delta.months > 0:
      return '%i month%s ago' % (delta.months, plural(delta.months))
  # if older than a week, show a formatted date.
  if delta.days > 7:
      return '%i week%s ago' % (delta.days / 7, plural(delta.days / 7))
  if delta.days > 0:
      return '%i day%s ago' % (delta.days, plural(delta.days))
  if delta.hours > 0:
      return short and \
              '%i hr%s ago' % (delta.hours, plural(delta.hours)) or \
              '%i hour%s ago' % (delta.hours, plural(delta.hours))
  if delta.minutes > 0:
      return short and \
              '%i min%s ago' % (delta.minutes, plural(delta.minutes)) or \
              '%i minute%s ago' % (delta.minutes, plural(delta.minutes))
  return 'just now'

def json(value):
  if value is None:
    return 'undefined'

  if isinstance(value, bool):
    return value and 'true' or 'false'

  if isinstance(value, (int, long, float)):
    return value

  # simplejson will fubar some unicode chars
  if isinstance(value, basestring):
    return '"%s"' % value.replace('\\', r'\\') \
                         .replace('"', r'\"') \
                         .replace('\n', r'\n') \
                         .replace('\r', r'\r')

  import simplejson
  return simplejson.dumps(value)
