from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytils.translit import slugify
from notes.models import Note
from yanote.common import BaseNotesTestSetup


User = get_user_model()

NOTES_ADD_URL = reverse('notes:add')


class TestNoteLogic(BaseNotesTestSetup):
    def test_anonymous_user_cannot_create_note(self):
        data = {
            'title': self.ANONYMOUS_NOTE_TITLE,
            'text': self.ANONYMOUS_NOTE_TEXT
        }

        response = self.anonymous_client.post(NOTES_ADD_URL, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            Note.objects.filter(title=self.ANONYMOUS_NOTE_TITLE).exists()
        )

    def test_logged_in_user_can_create_note(self):
        data = {
            'title': self.NEW_NOTE_TITLE,
            'text': self.NEW_NOTE_TEXT
        }

        response = self.client_author.post(NOTES_ADD_URL, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(title=self.NEW_NOTE_TITLE)
        self.assertEqual(note.author, self.author)
        self.assertTrue(note.slug)

    def test_cannot_create_notes_with_same_slug(self):
        Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='unique-slug',
            author=self.author
        )

        data = {
            'title': 'Другая заметка',
            'text': 'Текст',
            'slug': 'unique-slug'
        }

        response = self.client_author.post(self.NOTES_ADD_URL, data=data)

        form = response.context['form']
        self.assertFormError(
            form,
            'slug',
            'Заметка с таким slug уже существует.'
        )

    def test_slug_generated_if_not_provided(self):

        data = {
            'title': self.TEST_NOTE_TITLE,
            'text': self.TEST_NOTE_TEXT
        }

        response = self.client_author.post(NOTES_ADD_URL, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(title=self.TEST_NOTE_TITLE)
        expected_slug = slugify(self.TEST_NOTE_TITLE)
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):

        url_edit = reverse('notes:edit', args=(self.own_note.slug,))
        data_edit = {
            'title': self.EDITED_NOTE_TITLE,
            'text': self.EDITED_NOTE_TEXT
        }

        response = self.client_author.post(url_edit, data=data_edit)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.own_note.refresh_from_db()
        self.assertEqual(
            self.own_note.title,
            self.EDITED_NOTE_TITLE
        )

    def test_user_can_delete_own_note(self):

        url_delete = reverse(
            'notes:delete',
            args=(self.own_note.slug,)
        )

        response = self.client_author.post(url_delete)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            Note.objects.filter(slug=self.own_note.slug).exists()
        )

    def test_user_cannot_edit_others_note(self):
        url_edit = reverse(
            'notes:edit',
            args=(self.others_note.slug,)
        )
        data_edit = {
            'title': self.HACK_NOTE_TITLE,
            'text': self.HACK_NOTE_TEXT
        }

        response = self.client_author.post(url_edit, data=data_edit)

        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.others_note.refresh_from_db()
        self.assertEqual(
            self.others_note.title,
            self.OTHERS_NOTE_TITLE
        )

    def test_user_cannot_delete_others_note(self):
        url_delete = reverse(
            'notes:delete',
            args=(self.others_note.slug,)
        )

        response = self.client_author.post(url_delete)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(
            Note.objects.filter(slug=self.others_note.slug).exists()
        )
