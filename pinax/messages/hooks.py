from django.contrib.auth import get_user_model


class DefaultHookSet(object):

    def display_name(self, user):
        return str(user)

    def get_user_choices(self, user):
        return get_user_model().objects.exclude(id=user.id)


class HookProxy(object):
    _settings = None

    def load_settings(self):
        if self._settings is None:
            from .conf import settings
            self._settings = settings

    def __getattr__(self, attr):
        self.load_settings()
        return getattr(self._settings.PINAX_MESSAGES_HOOKSET, attr)


hookset = HookProxy()
