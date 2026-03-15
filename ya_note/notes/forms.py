from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Note


class NoteForm(forms.ModelForm):
    """Форма для создания или обновления заметки."""

    class Meta:
        model = Note
        fields = ('title', 'text', 'slug')

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        title = cleaned_data.get('title')

        if not slug:
            slug = slugify(title)
            cleaned_data['slug'] = slug

        if Note.objects.filter(
            slug=slug
        ).exclude(pk=self.instance.pk).exists():
            self.add_error('slug', 'Заметка с таким slug уже существует.')

        return cleaned_data