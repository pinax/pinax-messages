from django.contrib.auth import get_user_model


class DefaultHookSet(object):

    def display_name(self, user):
        return str(user)

    def get_user_choices(self, user):
        return get_user_model().objects.all()


class HookProxy(object):

    def load_settings(self):
        if not hasattr(self, "_settings"):
            from .conf import settings
            self._settings = settings

    def __getattr__(self, attr):
        self.load_settings()
        return getattr(self._settings.PINAX_MESSAGES_HOOKSET, attr)


hookset = HookProxy()
