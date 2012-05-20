from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.dispatch import dispatcher
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_protect

from profiles.forms import UserProfileForm
from common import render_to_response

@csrf_protect
def register(request):
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            django_login(request, user)
            return HttpResponseRedirect(reverse('common.views.home'))
    else:
        form = UserCreationForm()
    return render_to_response(request, 'register.html', {
        'form': form,
    })

@csrf_protect
def login(request):
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                print user
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('common.views.home'))
                else:
                    assert False, 'Account disabled'
            else:
                print 'user is None'
                pass
                # Return an 'invalid login' error message.
    else:
        form = AuthenticationForm()

    return render_to_response(request, 'login.html', {
        'form': form,
    })

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('common.views.home'))
