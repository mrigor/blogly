from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from jinja2 import Markup

from comments.forms import CommentForm
from comments.models import Comment
from comments.views import get_comments_page, get_thread_id
from common import render_to_remote_response, render_to_string

@login_required
def comment_reply(request, type, parent_id):
    parent_comment = Comment.objects.get(id=parent_id)
    response = {}
    if not parent_comment:
        response['error'] = 'Parent comment not found'
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = CommentForm(request.POST).save(commit=False)
            comment.thread_id, comment.reverse_thread_id = \
                    get_thread_id(type, parent_comment.thing_id, parent_comment)
            comment.author = request.user
            comment.thing_id = parent_comment.thing_id
            comment.type = type
            comment.parent_id = parent_comment.id
            comment.save()
            response['content'] = Markup.unescape(
                Markup(
                    render_to_string(request, 'comments/comment.html', {'comment': comment})
                )
            )

    return render_to_remote_response(request, json_context=response)

@login_required
def comment_edit(request, type, comment_id):
    response = {}
    if request.POST:
        comment = Comment.objects.get(id=comment_id)
        if not comment:
            response['error'] = 'Comment not found'
        else:
            if comment.author != request.user:
                response['error'] = 'Not your comment'
                return render_to_remote_response(request, json_context=response)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment.content = form.cleaned_data['content']
                comment.num_edits = comment.num_edits + 1
                comment.save()
                response['content'] = comment.content
    return render_to_remote_response(request, json_context=response)
