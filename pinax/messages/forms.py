from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Message


UserModel = get_user_model()


class NewMessageForm(forms.ModelForm):
    to_users = forms.ModelMultipleChoiceField(label=_("Recipients"), queryset=UserModel.objects.none())
    subject = forms.CharField(label=_("Subject"))
    content = forms.CharField(label=_("Content"), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["to_users"].queryset = (
            UserModel.objects.exclude(pk=self.user.pk).exclude(username="AnonymousUser").exclude(is_active=False)
        )

        if self.initial.get("to_users"):
            qs = self.fields["to_users"].queryset.filter(pk__in=self.initial["to_users"])
            self.fields["to_users"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.objects.new_message(self.user, data["to_users"], data["subject"], data["content"])

    class Meta:
        model = Message
        fields = ("to_users", "subject", "content")


class MessageReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        return Message.objects.new_reply(self.thread, self.user, self.cleaned_data["content"])

    class Meta:
        model = Message
        fields = ("content",)
