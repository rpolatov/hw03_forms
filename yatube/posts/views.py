from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post


def index(request):
    """Вывод на главной странице сообщества"""
    latest = Post.objects.all()
    paginator = Paginator(latest, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'posts': latest, 'page': page})


def group_posts(request, slug: object):
    """Вывод на главной странице Группы"""
    group = get_object_or_404(Group,
                              slug=slug)  # Ошибка "404",при неравенстве URL`ов
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html",
                  {"group": group, "posts": posts, 'page': page})


class PostView(CreateView):
    """Generic для вывода form`ы на страницу"""
    form_class = PostForm
    success_url = reverse_lazy('index')
    template_name = 'new.html'


@login_required  # Декоратор проверки авторизации
def new_post(request):
    """Функция создания нового поста для авторизированных пользователей"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Заполняем, но не сохраняем в БД.
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form})


@login_required
def profile(request, username):
    """ Профиль пользователя """
    user_r = get_object_or_404(User, username=username)
    posts = user_r.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'user_r': user_r, 'page': page})


def post_view(request, username, post_id):
    user_r = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'user_r': user_r, 'post': post})
