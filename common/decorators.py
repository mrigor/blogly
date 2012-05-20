from django.core.exceptions import PermissionDenied

def staff_only(function):
    def _inner(request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and not user.is_staff:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner
