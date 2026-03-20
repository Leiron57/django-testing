from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()

class BaseNotesTestSetup(TestCase):
    """Базовый класс для настройки тестовых данных заметок."""

    ANONYMOUS_NOTE_TITLE = 'Анонимная заметка'
    ANONYMOUS_NOTE_TEXT = 'Текст'

    NEW_NOTE_TITLE = 'Новая заметка'
    NEW_NOTE_TEXT = 'Текст заметки'

    TEST_NOTE_TITLE = 'Тестовая заметка'
    TEST_NOTE_TEXT = 'Текст'

    OWN_NOTE_TITLE = 'Моя заметка'
    OWN_NOTE_TEXT = 'Текст'

    OTHERS_NOTE_TITLE = 'Чужая заметка'
    OTHERS_NOTE_TEXT = 'Текст'

    EDITED_NOTE_TITLE = 'Обновлённая заметка'
    EDITED_NOTE_TEXT = 'Новый текст'

    HACK_NOTE_TITLE = 'Хак'
    HACK_NOTE_TEXT = 'Хак'

    UNIQUE_SLUG = 'unique-slug'
    OWN_NOTE_SLUG = 'my-note'
    OTHERS_NOTE_SLUG = 'others-note'

    SLUG_ERROR_MESSAGE = 'Заметка с таким slug уже существует.'

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='Пользователь1',
            password='testpass123'
        )
        cls.user2 = User.objects.create_user(
            username='Пользователь2',
            password='testpass123'
        )

        cls.note1 = Note.objects.create(
            title='Заметка1',
            text='Текст1',
            author=cls.user1
        )
        cls.note2 = Note.objects.create(
            title='Заметка2',
            text='Текст2',
            author=cls.user2
        )

        cls.author = User.objects.create(username='Автор')
        cls.other_user = User.objects.create(username='Чужой')

        cls.own_note = Note.objects.create(
            title='Заметка автора',
            text='Текст заметки автора',
            slug='author-note',
            author=cls.author
        )

        cls.others_note = Note.objects.create(
            title='Чужая заметка',
            text='Текст чужой заметки',
            slug='others-note',
            author=cls.other_user
        )

        cls.client_author = Client() 
        cls.client_author.force_login(cls.author)

        cls.client_user1 = Client()
        cls.client_user1.force_login(cls.user1)

        cls.client_user2 = Client()
        cls.client_user2.force_login(cls.user2)

        cls.anonymous_client = Client()

        cls.NOTES_HOME_URL = reverse('notes:home')
        cls.NOTES_LIST_URL = reverse('notes:list')
        cls.NOTES_ADD_URL = reverse('notes:add')
        cls.NOTES_SUCCESS_URL = reverse('notes:success')
        cls.USERS_LOGIN_URL = reverse('users:login')
        cls.USERS_SIGNUP_URL = reverse('users:signup')
        cls.USERS_LOGOUT_URL = reverse('users:logout')

        cls.NOTES_DETAIL_URL_ANONYMOUS = reverse('notes:detail', args=(cls.note1.slug,))
        cls.NOTES_EDIT_URL_ANONYMOUS = reverse('notes:edit', args=(cls.note1.slug,))
        cls.NOTES_DELETE_URL_ANONYMOUS = reverse('notes:delete', args=(cls.note1.slug,))

        cls.NOTES_DETAIL = reverse('notes:detail', args=(cls.own_note.slug,))
        cls.NOTES_EDIT = reverse('notes:edit', args=(cls.own_note.slug,))
        cls.NOTES_DELETE = reverse('notes:delete', args=(cls.own_note.slug,))
