from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .hooks import hookset
from .models import Message


class UserModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


class NewMessageForm(forms.ModelForm):

    subject = forms.CharField()
    to_user = UserModelChoiceField(queryset=get_user_model().objects.none())
    content = forms.CharField(widget=forms.Textarea)

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
        fields = ["to_user", "subject", "content"]


class NewMessageFormMultiple(forms.ModelForm):
    subject = forms.CharField()
    to_user = UserModelMultipleChoiceField(get_user_model().objects.none())
    content = forms.CharField(widget=forms.Textarea)

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
        fields = ["to_user", "subject", "content"]


class NewMessageFormMultipleGroup(forms.ModelForm):
    """
        This form provides the ability to send to both multiple users and
        multiple groups.

        If a group or groups are selected, a lookup is performed to get all users
        from the group(s) and send that list to Message.new_message().  If a user
        or multiple users are also selected the user(s) will be added to the list.
    """
    subject = forms.CharField()
    to_user = UserModelMultipleChoiceField(get_user_model().objects.none(),
        required=False)
    to_group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
        required=False)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageFormMultipleGroup, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk__in=self.initial["to_user"])
            self.fields["to_user"].queryset = qs

        if self.initial.get("to_group") is not None:
            qs = self.fields["to_group"].queryset.filter(pk__in=self.initial["to_group"])
            self.fields["to_group"].queryset = qs

    def clean(self):
        cleaned_data = super(NewMessageFormMultipleGroup, self).clean()
        to_user = cleaned_data.get('to_user')
        to_group = cleaned_data.get('to_group')

        if not to_user and not to_group:
            msg = "Please select either some users or some groups"
            self.add_error('to_user', msg)
            self.add_error('to_group', msg)

    def save(self, commit=True):
        data = self.cleaned_data
        users = None
        if data['to_group']:
            users = get_user_model().objects.filter(
                groups__name__in=data['to_group'].values_list('name'))

        if users:
            sendto = data['to_user'].union(users)
        else:
            sendto = data['to_user']

        return Message.new_message(
            self.user, sendto, data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "to_group", "subject", "content"]


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
        fields = ["content"]
