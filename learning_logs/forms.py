from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'is_public']
        labels = {'text': '', 'is_public': 'Public'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class DeleteTopicForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm your password to delete this topic"
    )
