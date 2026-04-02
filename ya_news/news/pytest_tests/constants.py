from django.conf import settings
from django.urls import reverse

WARNING = 'Не ругайтесь!'

BAD_WORDS = (
    'редиска',
    'негодяй',
)


NEWS_COUNT_FOR_TESTING = settings.NEWS_COUNT_ON_HOME_PAGE + 1


HOME_URL = 'news:home'
USER_LOGIN = 'users:login'
USER_SIGNUP = 'users:signup'
USER_LOGOUT = 'users:logout'
NEWS_DETAIL_URL = 'news:detail'
NEWS_EDIT_URL = 'news:edit'
NEWS_DELETE_URL = 'news:delete'
NEWS_COMMENT_URL = 'news:comment'


def get_home_url():
    return reverse(HOME_URL)


def get_detail_url(news):
    return reverse(NEWS_DETAIL_URL, args=(news.pk,))


def get_comment_url(news):
    return reverse(NEWS_COMMENT_URL, args=(news.pk,))


def get_edit_url(comment):
    return reverse(NEWS_EDIT_URL, args=(comment.pk,))


def get_delete_url(comment):
    return reverse(NEWS_DELETE_URL, args=(comment.pk,))


def get_detail_with_comments_url(news):
    return f'{reverse(NEWS_DETAIL_URL, args=(news.pk,))}#comments'


def get_login_url():
    return reverse(USER_LOGIN)


def get_logout_url():
    return reverse(USER_LOGOUT)


def get_signup_url():
    return reverse(USER_SIGNUP)
