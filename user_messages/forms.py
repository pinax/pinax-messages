from django import forms

from django.contrib.auth.models import User

from user_messages.models import Message


class NewMessageForm(forms.Form):
    
    subject = forms.CharField()
    to_user = forms.ModelChoiceField(User.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageForm, self).__init__(*args, **kwargs)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk=self.initial["to_user"])
            self.fields["to_user"].queryset = qs
    
    def save(self):
        data = self.cleaned_data
        return Message.objects.new_message(self.user, [data["to_user"]],
            data["subject"], data["content"])


class NewMessageFormMultiple(forms.Form):
    
    subject = forms.CharField()
    to_user = forms.ModelMultipleChoiceField(User.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageFormMultiple, self).__init__(*args, **kwargs)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk__in=self.initial["to_user"])
            self.fields["to_user"].queryset = qs
    
    def save(self):
        data = self.cleaned_data
        return Message.objects.new_message(self.user, data["to_user"],
            data["subject"], data["content"])


class MessageReplyForm(forms.Form):
    
    content = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super(MessageReplyForm, self).__init__(*args, **kwargs)
    
    def save(self):
        return Message.objects.new_reply(self.thread, self.user,
            self.cleaned_data["content"])
