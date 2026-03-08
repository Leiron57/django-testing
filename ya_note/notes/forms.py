from pytils.translit import slugify

from django import forms
from django.core.exceptions import ValidationError

from .models import Note

WARNING = ' - такой slug уже существует, придумайте уникальное значение!'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'slug')
        widgets = {'slug': forms.HiddenInput()}  # скрываем поле от пользователя

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            title = self.cleaned_data.get('title')
            slug = slugify(title)[:100]

        if Note.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Такой slug уже существует!')

        return slug
