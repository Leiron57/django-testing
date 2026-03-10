from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import CommentForm
from .models import Comment, News


class NewsList(generic.ListView):
    """Список новостей."""
    model = News
    template_name = 'news/home.html'

    def get_queryset(self):
        return self.model.objects.prefetch_related(
            'comment_set'
        )[:settings.NEWS_COUNT_ON_HOME_PAGE]


class NewsDetail(generic.DetailView):
    model = News
    template_name = 'news/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.prefetch_related(
                'comment_set__author'
            ),
            pk=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.object
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


class NewsComment(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.FormView):
    model = News
    form_class = CommentForm
    template_name = 'news/detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # News object
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.news = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Гарантированно используем self.object
        if not self.object:
            return reverse('news:home') + '#comments'
        return reverse('news:detail', kwargs={'pk': self.object.pk}) + '#comments'


class NewsDetailView(generic.View):
    """Объединяет GET (просмотр) и POST (создание комментария)."""

    def get(self, request, *args, **kwargs):
        view = NewsDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            view = NewsDetail.as_view()
            return view(request, *args, **kwargs)

        view = NewsComment.as_view()
        return view(request, *args, **kwargs)


class CommentBase(LoginRequiredMixin):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404
        return obj


class CommentUpdate(CommentBase, generic.UpdateView):
    """Редактирование комментария."""
    template_name = 'news/edit.html'
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        return (
            reverse_lazy('news:detail', args=(self.object.news.pk,))
            + '#comments'
        )


class CommentDelete(CommentBase, generic.DeleteView):
    """Удаление комментария."""
    template_name = 'news/delete.html'
