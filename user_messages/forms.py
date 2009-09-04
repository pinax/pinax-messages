from django import forms

from user_messages.models import Thread, Message

class NewMessageForm(forms.ModelForm):
    subject = forms.CharField()
    
    class Meta:
        model = Message
        fields = ('to_user', 'content')
    
    def save(self, commit=True, user=None):
        obj = super(NewMessageForm, self).save(commit=False)
        obj.from_user = user
        # TODO: the Thread get's saved whether or not commit=True, is there a 
        # better way?
        obj.thread = Thread.objects.create(subject=self.cleaned_data['subject'])
        if commit:
            obj.save()
        return obj
