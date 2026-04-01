from django.urls import reverse
from django.conf import settings


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