import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from articles.models import UsersRating, Article
from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User, Subscription
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
class Profile(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'object'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('articles__comments')

    def dispatch(self, request, *args, **kwargs):
        is_subscribe: bool = request.user.is_subscribed(self.get_object())
        self.extra_context = {
            'is_subscribe': is_subscribe
        }
        return super().dispatch(request, args, kwargs)

class Edit(TemplateView):
    template_name = 'users/edit.html'

def change_photo(request):
    if request.method == 'POST':
        user = request.user
        new_photo = request.FILES.get('new_photo')
        if user.photo != 'images/user/default.jpg':
            old_photo_path = os.path.join(settings.MEDIA_ROOT, str(user.photo))
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
        user.photo = new_photo
        user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def change_password(request):
    if request.method == 'POST':
        user = request.user
        old = request.POST.get('old_pass')
        new = request.POST.get('new_pass')
        repeat = request.POST.get('repeat_pass')
        if check_password(old, user.password):
            if new == repeat:
                user.password = make_password(new)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен!')
            else:
                messages.error(request, 'Пароли не совпадают!')
        else:
            messages.error(request, 'Старый пароль неверный!')

    return redirect(request.META.get('HTTP_REFERER', '/'))

class Subscriptions(DetailView):
    model = User
    template_name = 'users/subscriptions.html'
    context_object_name = 'object'
    
    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_rating = UsersRating.objects.filter(user=request.user).prefetch_related('article')
        dict_of_rating = {r.article.pk:r.rate for r in user_rating}

        subscriptions = Subscription.objects.filter(user=request.user).prefetch_related('subscribed_to')
        subscriptions_val = subscriptions.values('subscribed_to')
        subscribe_articles = Article.objects.filter(
            author__in=subscriptions_val
        ).select_related('author').prefetch_related('comments')

        self.extra_context = {
            'user_rating': dict_of_rating, 
            'articles': subscribe_articles,
            'subscriptions': subscriptions
        }
        return super().dispatch(request, *args, **kwargs)

def search_user(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        if not username == '': 
            users = User.objects.filter(username__icontains=username)
            user_list = [
                {
                    'username': user.username,
                    'photo_url': user.photo.url,
                    'id': user.pk
                }
                for user in users
            ]
            return JsonResponse({'users':user_list})

@login_required
def subscribe(request, pk):
    Subscription(user=request.user, subscribed_to=get_object_or_404(User, pk=pk)).save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsubscribe(request, pk):
    Subscription.objects.filter(user=request.user, subscribed_to=get_object_or_404(User, pk=pk)).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))