from django import forms
from .models import Comment
import re
from news.pytest_tests.constants import WARNING, BAD_WORDS


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        for bad_word in BAD_WORDS:
            if re.search(rf'\b{re.escape(bad_word)}\b', text, re.IGNORECASE):
                raise forms.ValidationError(WARNING)
        return text
