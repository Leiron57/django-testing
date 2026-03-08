from django.urls import path

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsList.as_view(), name='home'),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='detail'),
    path(
        'delete_comment/<int:pk>/',
        views.CommentDelete.as_view(),
        name='delete'
    ),
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view(), name='edit'),
]
