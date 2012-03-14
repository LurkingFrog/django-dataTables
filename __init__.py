
# This was imported from django's admin and updated to work for this app
def autodiscover():
    """
    Auto-discover INSTALLED_APPS dt_forms.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            import_module('%s.dt_forms' % app)

        except Exception:
            pass
