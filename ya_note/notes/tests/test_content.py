from .common import BaseNotesTestSetup
from notes.forms import NoteForm


class TestNotesContent(BaseNotesTestSetup):

    def test_notes_list_contains_object_list_key(self):
        """Проверяет, что в контексте списка заметок есть ключ object_list."""
        response = self.client_user1.get(self.NOTES_LIST_URL)
        self.assertIn('object_list', response.context)

    def test_user1_sees_own_note_in_list(self):
        """Проверяет, что пользователь 1 видит свою заметку в списке."""
        response = self.client_user1.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)

    def test_user1_does_not_see_other_user_note(self):
        """Проверяет, что пользователь 1 не видит заметку пользователя 2."""
        response = self.client_user1.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note2, object_list)

    def test_user2_sees_own_note_in_list(self):
        """Проверяет, что пользователь 2 видит свою заметку в списке."""
        response = self.client_user2.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note2, object_list)

    def test_user2_does_not_see_other_user_note(self):
        """Проверяет, что пользователь 2 не видит заметку пользователя 1."""
        response = self.client_user2.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note1, object_list)

    def test_create_note_page_contains_form(self):
        """Проверяет, что страница создания заметки содержит форму."""
        response = self.client_user1.get(self.NOTES_ADD_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        """Проверяет, что страница редактирования заметки содержит форму."""
        response = self.client_user1.get(self.NOTES_ADD_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
