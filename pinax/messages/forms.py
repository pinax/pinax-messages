from django import forms

from django.contrib.auth import get_user_model

from .hooks import hookset
from .models import Message


class NewMessageForm(forms.ModelForm):
    subject = forms.CharField()
    to_user = forms.ModelChoiceField(queryset=get_user_model().objects.none)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk=self.initial["to_user"])
            self.fields["to_user"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, [data["to_user"]], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ['to_user', 'subject', 'content']


class NewMessageFormMultiple(forms.ModelForm):
    subject = forms.CharField()
    to_user = forms.ModelMultipleChoiceField(get_user_model().objects.none)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageFormMultiple, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk__in=self.initial["to_user"])
            self.fields["to_user"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, data["to_user"], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ['to_user', 'subject', 'content']


class MessageReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super(MessageReplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return Message.new_reply(
            self.thread, self.user, self.cleaned_data["content"]
        )

    class Meta:
        model = Message
        fields = ['content']
