from django.urls import reverse

from yanote.common import BaseNotesTestSetup

from notes.forms import NoteForm


class TestNotesContent(BaseNotesTestSetup):

    def test_note_in_list_context(self):
        response = self.client_user1.get(self.NOTES_LIST_URL)

        self.assertIn('object_list', response.context)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)
        self.assertNotIn(self.note2, object_list)

    def test_user_sees_only_own_notes(self):

        response_user1 = self.client_user1.get(self.NOTES_LIST_URL)
        response_user2 = self.client_user2.get(self.NOTES_LIST_URL)
        notes_user1 = response_user1.context['object_list']
        notes_user2 = response_user2.context['object_list']

        self.assertIn(self.note1, notes_user1)
        self.assertNotIn(self.note2, notes_user1)

        self.assertIn(self.note2, notes_user2)
        self.assertNotIn(self.note1, notes_user2)

    def test_note_form_in_create(self):

        response_add = self.client_user1.get(self.NOTES_ADD_URL)

        self.assertIn('form', response_add.context)
        self.assertIsInstance(response_add.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        response_edit = self.client_user1.get(self.NOTES_ADD_URL)

        self.assertIn('form', response_edit.context)
        self.assertIsInstance(response_edit.context['form'], NoteForm)
