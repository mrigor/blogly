import os
import imp
import warnings

# Include the local settings in the following order:
# 1. standard_settings.py
# 2. opt/localsettings/<env>/settings.py
# 3. local_settings.py

def _magic_function(settings):
    # I copy everything that DJANGO cares about to this module's globals.
    globals().update((k,v) for k,v in vars(settings).iteritems() if k == k.upper())

# load up the normal settings
import standard_settings as _settings
# make them accessable everywhere, in particular, inside the various
# local_settings modules :)
__builtins__['_settings'] = _settings
# update the local scope
_magic_function(_settings)

# a local_settings.py module is not optional.
import local_settings

_environment = getattr(local_settings, 'ENVIRONMENT', None)
# support overriding the environment via env var
_environment = os.environ.get('DJANGO_SETTINGS_ENVIRONMENT', _environment) or _environment
local_settings.ENVIRONMENT = _environment

# add the user's real local_settings
_magic_function(local_settings)
del local_settings
