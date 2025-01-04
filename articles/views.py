from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Article, UsersRating
from users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleForm, CommentForm


class Main(ListView):
    model = Article
    template_name = 'index.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('comments').select_related('author')

    def dispatch(self, request, *args, **kwargs):
        dict_of_rating = {}
        if request.user.is_authenticated:
            user_rating = UsersRating.objects.filter(user=request.user)
            dict_of_rating = {r.article.pk:r.rate for r in user_rating}
            user_articles = request.user.articles.prefetch_related('comments').all()
        else:
            user_articles = None
        self.extra_context = {
            'user_rating': dict_of_rating,
            'form': ArticleForm(),
            'user_articles':user_articles
        }
        return super().dispatch(request, *args, **kwargs)

class DetailArticle(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'obj'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('comments__user').prefetch_related('author__articles__comments')

    def dispatch(self, request, *args, **kwargs):
        dict_of_rating = {}
        if request.user.is_authenticated:
            user_rating = UsersRating.objects.filter(user=request.user)
            dict_of_rating = {r.article.pk:r.rate for r in user_rating}
        self.extra_context = {
            'user_rating': dict_of_rating,
            'form': CommentForm(),
        }
        return super().dispatch(request, *args, **kwargs)

@login_required
def create_comment(request, article):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = get_object_or_404(Article, pk=article)
        comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def create_article(request):
    form = ArticleForm(request.POST, request.FILES)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
    return redirect('index')

'''
∫Переопределить метод delete
- делать update_rating
- удалять фото физически если есть
'''
@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('index')

@login_required
def rate_article(request, pk, star):
    article = get_object_or_404(Article, pk=pk)

    try:
        UsersRating.objects.create(user=request.user, article=article, rate=star)
    except IntegrityError:
        rating = UsersRating.objects.get(user=request.user, article=article)
        if rating.rate == star:
            rating.delete()
        else:
            rating.rate = star
            rating.save()

    User.objects.get(pk=article.author.pk).update_rating()

    return redirect(request.META.get('HTTP_REFERER', '/'))
