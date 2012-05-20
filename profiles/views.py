from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect

from blog.models import Blog
from profiles.forms import UserProfileForm
from common import render_to_response

def profile(request, user_id=None):
    if not user_id:
        user_id = request.user.id
    user = User.objects.get(id=user_id)
    if not user:
        raise Http404

    blogs = Blog.objects \
            .filter(author=request.user) \
            .all()[:10]


    return render_to_response(request, 'profiles/profile.html', {
        'user': user,
        'blogs': blogs,
    })

@login_required
def profile_save(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user != user:
        raise Http404
    if request.POST:
        form = UserProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profiles.views.profile', kwargs={'user_id': user.id}))
    else:
        form = UserProfileForm(instance=user.profile)

    return render_to_response(request, 'profiles/profile_save.html', {
        'form': form,
    })
