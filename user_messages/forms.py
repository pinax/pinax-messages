from django import forms

from user_messages.models import Thread, Message

class NewMessageForm(forms.ModelForm):
    subject = forms.CharField()
    
    class Meta:
        model = Message
        fields = ('to_user', 'content')
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewMessageForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        obj = super(NewMessageForm, self).save(commit=False)
        obj.from_user = self.user
        # TODO: the Thread get's saved whether or not commit=True, is there a 
        # better way?
        obj.thread = Thread.objects.create(subject=self.cleaned_data['subject'])
        if commit:
            obj.save()
        return obj

class MessageReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread')
        self.user = kwargs.pop('user')
        super(MessageReplyForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        obj = super(MessageReplyForm).save(commit=False)
