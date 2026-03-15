from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from pytils.translit import slugify


User = get_user_model()


class TestNoteLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_user = User.objects.create(username='Чужой')

        cls.client_author = Client()
        cls.client_author.force_login(cls.author)

        cls.client_other = Client()
        cls.client_other.force_login(cls.other_user)

        cls.anonymous_client = Client()

    def test_anonymous_user_cannot_create_note(self):
        url = reverse('notes:add')
        data = {'title': 'Анонимная заметка', 'text': 'Текст'}
        response = self.anonymous_client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            Note.objects.filter(title='Анонимная заметка').exists()
        )

    def test_logged_in_user_can_create_note(self):
        url = reverse('notes:add')
        data = {'title': 'Новая заметка', 'text': 'Текст заметки'}
        response = self.client_author.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(title='Новая заметка')
        self.assertEqual(note.author, self.author)
        self.assertTrue(note.slug)

    def test_cannot_create_notes_with_same_slug(self):
        Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='unique-slug',
            author=self.author
        )

        url = reverse('notes:add')
        data = {
            'title': 'Другая заметка',
            'text': 'Текст',
            'slug': 'unique-slug'
        }

        response = self.client_author.post(url, data=data)

        form = response.context['form']
        self.assertFormError(
            form,
            'slug',
            'Заметка с таким slug уже существует.'
        )

    def test_slug_generated_if_not_provided(self):
        url = reverse('notes:add')
        data = {'title': 'Тестовая заметка', 'text': 'Текст'}
        response = self.client_author.post(url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        note = Note.objects.get(title='Тестовая заметка')
        expected_slug = slugify('Тестовая заметка')

        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_and_delete_own_note(self):
        note = Note.objects.create(
            title='Моя заметка',
            text='Текст',
            author=self.author
        )
        url_edit = reverse('notes:edit', args=(note.slug,))
        data_edit = {'title': 'Обновлённая заметка', 'text': 'Новый текст'}
        response = self.client_author.post(url_edit, data=data_edit)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note.refresh_from_db()
        self.assertEqual(note.title, 'Обновлённая заметка')
        url_delete = reverse('notes:delete', args=(note.slug,))
        response = self.client_author.post(url_delete)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(slug=note.slug).exists())

    def test_user_cannot_edit_or_delete_others_note(self):
        note = Note.objects.create(
            title='Чужая заметка',
            text='Текст',
            author=self.other_user
        )
        url_edit = reverse('notes:edit', args=(note.slug,))
        response = self.client_author.post(
            url_edit,
            data={
                'title': 'Хак',
                'text': 'Хак',
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note.refresh_from_db()
        self.assertEqual(note.title, 'Чужая заметка')
        url_delete = reverse('notes:delete', args=(note.slug,))
        response = self.client_author.post(url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(slug=note.slug).exists())
