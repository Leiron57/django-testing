from django.urls import reverse

WARNING = 'Не ругайтесь!'

BAD_WORDS = (
    'редиска',
    'негодяй',
    # Дополните список на своё усмотрение.
)

HOME_URL = reverse('news:home')
