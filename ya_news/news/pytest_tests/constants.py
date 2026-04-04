from django.conf import settings
from django.urls import reverse

WARNING = 'Не ругайтесь!'

BAD_WORDS = (
    'редиска',
    'негодяй',
)


NEWS_COUNT_FOR_TESTING = settings.NEWS_COUNT_ON_HOME_PAGE + 1


NEWS_DETAIL_URL = 'news:detail'
NEWS_EDIT_URL = 'news:edit'
NEWS_DELETE_URL = 'news:delete'
NEWS_COMMENT_URL = 'news:comment'


HOME_URL = reverse('news:home')
USER_LOGIN_URL = reverse('users:login')
USER_SIGNUP_URL = reverse('users:signup')
USER_LOGOUT_URL = reverse('users:logout')
