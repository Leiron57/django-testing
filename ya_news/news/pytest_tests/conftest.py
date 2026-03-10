import os
import django
import sys
from pathlib import Path

# === 1. Добавляем корень проекта в PYTHONPATH ===
# Получаем путь к ~/Dev/django-testing/ya_news
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# === 2. Указываем правильный модуль настроек ===
# Так как settings.py лежит в yanews/settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ya_news.yanews.settings')

# === 3. Инициализируем Django ===
django.setup()

# === 4. Теперь можно импортировать модели ===
from django.contrib.auth import get_user_model
from news.models import News, Comment


# === 5. Фикстуры ===
import pytest

@pytest.fixture
def author():
    User = get_user_model()
    return User.objects.create(username='Автор')


import pytest

@pytest.fixture
def not_author():
    User = get_user_model()
    return User.objects.create(username='Не автор')


import pytest

@pytest.fixture
def author_client(author):
    from django.test import Client
    client = Client()
    client.force_login(author)
    return client


import pytest

@pytest.fixture
def not_author_client(not_author):
    from django.test import Client
    client = Client()
    client.force_login(not_author)
    return client


import pytest

@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
        author=author,
    )


import pytest

@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )