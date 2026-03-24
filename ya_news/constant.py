from django.urls import reverse
from django.conf import settings


WARNING = 'Не ругайтесь!'

BAD_WORDS = (
    'редиска',
    'негодяй',
)

HOME_URL = reverse('news:home')

NEWS_COUNT_FOR_TESTING = settings.NEWS_COUNT_ON_HOME_PAGE + 1

def get_news_detail_url(news_pk):
    return reverse('news:detail', args=(news_pk,))