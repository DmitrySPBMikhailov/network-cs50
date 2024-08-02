from django.forms import ModelForm
from django import forms
from .models import Post
from crispy_forms.helper import FormHelper


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 2, 'cols': 10})}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False