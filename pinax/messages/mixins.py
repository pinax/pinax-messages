from django.contrib.auth.mixins import LoginRequiredMixin


class PinaxMessageBaseAuthMixin(LoginRequiredMixin):
    """
    This mixin is a replacement for the login_required decorator used.
    Pinax Messages uses as a base to apply possible common functionalities
    across views in the project and to make the code consistent and
    maintainable.
    """
    pass
