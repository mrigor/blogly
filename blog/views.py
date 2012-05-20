from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from common import render_to_response
from common.decorators import staff_only
from common.paging import Page

from blog.forms import BlogForm
from blog.models import Blog
from comments.forms import CommentForm
from comments.views import get_comments_page, get_thread_id

@login_required
@staff_only
def blog_save(request, slug=None):
    blog = None
    if slug:
        blog = Blog.objects.get(slug=slug)
        if not blog or blog.author_id != request.user.id:
            raise Http404

    if request.POST:
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = BlogForm(form.cleaned_data, instance=blog).save(commit=False)
            if not slug:
                blog.is_active = True
                blog.author = request.user
            blog.save()
            return HttpResponseRedirect(
                reverse('blog.views.blog', kwargs={'slug': blog.slug}))
    else:
        form = BlogForm(instance=blog)

    return render_to_response(request, 'blog/blog_save.html', {
        'form': form,
        'blog': blog,
    })

def get_blogs_page(request, rpp=10, author=None):
    blogs_list = Blog.objects
    if author:
        blogs_list = blogs_list.filter(author=author)
    blogs_list = blogs_list.order_by('-created_ts').all()

    blogs = Page(blogs_list, rpp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        blogs = blogs.page(page)
    except (EmptyPage, InvalidPage):
        blogs = blogs.page(blogs.num_pages)

    return blogs

def blog(request, slug):
    from comments.models import BLOG
    blog = Blog.objects.get(slug=slug)
    if not blog:
        raise Http404
    form = CommentForm()
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thing_id = blog.id
            comment.type = BLOG
            comment.thread_id, comment.reverse_thread_id = \
                    get_thread_id(type='blog', thing_id=blog.id)
            comment.save()
            return HttpResponseRedirect(reverse(
                'blog.views.blog',
                args=(blog.slug,)))

    commentsPage, commentsIndex, commentsTree = \
        get_comments_page(request, type=BLOG, obj=blog, rpp=10)

    return render_to_response(request, 'blog/blog.html', {
        'blog': blog,
        'commentForm': form,
        'comments': commentsPage,
        'commentsIndex': commentsIndex,
        'commentsTree': commentsTree,
    })

def blogs(request):
    blogs = get_blogs_page(request)

    return render_to_response(request, 'blog/blogs.html', {
        'blogs': blogs,
    })
