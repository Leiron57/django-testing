from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestNotesContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='Пользователь1')
        cls.user2 = User.objects.create(username='Пользователь2')

        cls.note1 = Note.objects.create(title='Заметка1', text='Текст1', author=cls.user1)
        cls.note2 = Note.objects.create(title='Заметка2', text='Текст2', author=cls.user2)

        cls.client_user1 = Client()
        cls.client_user1.force_login(cls.user1)

        cls.client_user2 = Client()
        cls.client_user2.force_login(cls.user2)


    def test_note_in_list_context(self):
        url = reverse('notes:list')
        response = self.client_user1.get(url)
        self.assertIn('object_list', response.context)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)
        self.assertNotIn(self.note2, object_list)


    def test_user_sees_only_own_notes(self):
        url = reverse('notes:list')
        response_user1 = self.client_user1.get(url)
        response_user2 = self.client_user2.get(url)
        notes_user1 = response_user1.context['object_list']
        notes_user2 = response_user2.context['object_list']

        self.assertIn(self.note1, notes_user1)
        self.assertNotIn(self.note2, notes_user1)

        self.assertIn(self.note2, notes_user2)
        self.assertNotIn(self.note1, notes_user2)


    def test_note_form_in_create_and_edit(self):
        url_add = reverse('notes:add')
        response_add = self.client_user.get(url_add)
        self.assertIn('form', response_add.context)
        self.assertIsInstance(response_add.context['form'], NoteForm)

        url_edit = reverse('notes:edit', args=(self.note.slug,))
        response_edit = self.client_user.get(url_edit)
        self.assertIn('form', response_edit.context)
        self.assertIsInstance(response_edit.context['form'], NoteForm)