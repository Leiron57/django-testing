from django.urls import reverse
from django.conf import settings


WARNING = 'Не ругайтесь!'

BAD_WORDS = (
    'редиска',
    'негодяй',
)

HOME_URL = reverse('news:home')

NEWS_COUNT_FOR_TESTING = settings.NEWS_COUNT_ON_HOME_PAGE + 1


NEWS_DETAIL_URL = 'news:detail'
NEWS_COMMENT_URL = 'news:comment'
NEWS_EDIT_URL = 'news:edit'
NEWS_DELETE_URL = 'news:delete'


def get_news_detail_url(news_pk):
    return reverse(NEWS_DETAIL_URL, args=(news_pk,))


def get_news_comment_url(news_pk):
    return reverse(NEWS_COMMENT_URL, args=(news_pk,))


def get_comment_edit_url(comment_pk):
    return reverse(NEWS_EDIT_URL, args=(comment_pk,))


def get_comment_delete_url(comment_pk):
    return reverse(NEWS_DELETE_URL, args=(comment_pk,))


def get_news_detail_with_comments_url(news_pk):
    return f'{reverse(NEWS_DETAIL_URL, args=(news_pk,))}#comments'
