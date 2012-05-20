import os
from os import path

from django.conf import settings
from django.http import HttpResponse
from django.template.context import get_standard_processors
from django.views.debug import ExceptionReporter
from django.utils.html import escape

from jinja2 import Environment, BytecodeCache, TemplateError
from jinja2.loaders import FileSystemLoader

from util import filters, functions

class JinjaCache(BytecodeCache):

    def __init__(self, directory):
        self.directory = directory

    def load_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        if path.exists(filename):
            with open(filename, 'rb') as f:
                bucket.load_bytecode(f)

    def dump_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        with open(filename, 'wb') as f:
            bucket.write_bytecode(f)

env = None

def initialize():
    """ Initialize jinja """
    global env

    if env:
        print "Jinja already initialized."
        return

    #create directory to store bytecode
    if not os.path.isdir(settings.BYTECODE_CACHE_DIR):
        os.makedirs(settings.BYTECODE_CACHE_DIR, 0777)

    # setup environment
    env = Environment(
        loader=FileSystemLoader(settings.TEMPLATE_DIRS),
        auto_reload=settings.DEBUG,
        bytecode_cache=JinjaCache(directory=settings.BYTECODE_CACHE_DIR),
        autoescape=False,
        extensions=['jinja2.ext.autoescape'], # gives {% autoescape false %} block
    )

    # register filters
    env.filters.update(dict([
        (key, value) for key, value in filters.__dict__.items()
        if not key.startswith('__') and callable(value)]
    ))

    # register functions
    env.globals.update(dict([
        (key, value) for key, value in functions.__dict__.items()
        if not key.startswith('__') and callable(value)]
    ))

    # register unique identifier for static content references
    env.globals['STATIC_UID'] = settings.CODE_REVISION

    # if variable is None print '' instead of 'None'
    def _silent_none(value):
        if value is None:
            return ''
        return value
    env.finalize = _silent_none

    #Fix exception handling in django
    # from http://www.google.com/codesearch/p?hl=en#ynWOvf_bgl8/djangosnippets/jinja2/djangojinja2.py&q=get_template_exception_info
    _origin_get_template_exception_info = ExceptionReporter.get_template_exception_info
    def _get_template_exception_info(self):
        if(not isinstance(self.exc_value, TemplateError)):
            return _origin_get_template_exception_info(self)
        #origin, (start, end) = self.exc_value.source
        f = open(self.exc_value.filename, 'r')
        source_lines = f.readlines()
        f.close()
        line = self.exc_value.lineno
        during = escape(source_lines[line - 1])
        source_lines = [(num + 1, escape(v)) for num, v in enumerate(source_lines)]
        context_lines = 10
        #before = during = after = ""
        total = len(source_lines)
        top = max(1, line - context_lines)
        bottom = min(total, line + 1 + context_lines)

        self.template_info = {
            'message': self.exc_value.args[0],
            'source_lines': source_lines[top - 1:bottom - 1],
            'before': "",
            'during': during,
            'after': "",
            'top': top,
            'bottom': bottom,
            'total': total,
            'line': line,
            'name': self.exc_value.name,
        }
    ExceptionReporter.get_template_exception_info = _get_template_exception_info

def render_to_response(request, template, context=None,
    mimetype=settings.DEFAULT_CONTENT_TYPE, response=HttpResponse):
    content = render_to_string(request, template, context)
    return response(content, mimetype)

def render_to_string(request, template, ctxt=None):
    """Render a template to a string."""
    context = ctxt if ctxt is not None else {}
    if request is not None:
        context['request'] = request
        # skip non essential context processors for error pages
        if template not in ('404.html', '500.html'):
            # include django context processors
            for processor in get_standard_processors():
                for key, value in processor(request).items():
                    if key not in context:
                        context[key] = value
        else:
            from django.core.context_processors import request as django_request
            from extensions.context_processors import settings_
            processors = (django_request, settings_)
            for processor in processors:
                for key, value in processor(request).items():
                    if key not in context:
                        context[key] = value

    template = env.get_template(template)
    return template.render(context)

def render_to_remote_response(request,
    json_template='default.json', json_context=None,
    content_template=None, content_context=None, mimetype='application/txt',
    response_class=HttpResponse):
    """
    Function to generate a json response for remote ajax calls.
    """
    if json_context is None:
      json_context = {}

    content = None
    if content_template:
         content_context = content_context or {}
         content_context['request'] = request
         content_context['user'] = request.user
         content = render_to_string(request, content_template, content_context)
         json_context['content'] = content
    json_context['context'] = json_context.copy()
    response = render_to_string(request, json_template, json_context)
    return response_class(response, mimetype=mimetype)

initialize()
