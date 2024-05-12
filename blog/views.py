from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import MyUserCreationForm, LoginForm, PostForm, CommentForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_user(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, 'Username already taken')
            else:
                user.username = user.username.lower()
                user.save()
                login(request, user)
                messages.success(request, f"Welcome '{user.username}'!👋 your account has been created successfully!")
                return redirect('post_list')
    context = {'form': form}
    return render(request, 'blog/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                print('next_url:', next_url)
                return redirect(next_url)
            else:
                messages.error(request, 'invalid username or password 😕')
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'blog/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('post_list')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    # post = Post.objects.get(pk=pk) this code will throw query error if the pk does not exist
    post = get_object_or_404(Post, id=pk) # the code will throw page not found if the pk does not exist. will display much nicer page.
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required(login_url='login')
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='login')
def post_draft_list(request):
    not_published_posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    
    context = {'not_published_posts': not_published_posts}
    return render(request, 'blog/post_draft_list.html', context)


@login_required(login_url='login')
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required(login_url='login')
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.id == post.author.id:
        post.delete()
        messages.success(request, 'Your post has been deleted successfully 🚮')
    else:
        messages.error(request, 'Only the author can delete the post! 👿')

    return redirect('post_list')


@login_required(login_url='login')
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post 
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required(login_url='login')
def comment_approve(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser:
        comment.approve()
    else:
        messages.error(request, '🔒 only the owner of blog can approve comments 🔒')

    return redirect('post_detail', pk=comment.post.pk)


@login_required(login_url='login')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.id == comment.author.id or request.user.is_superuser:
        comment.delete()
    else:
        messages.error(request, 'You\'re not the author of the comment.')
    
    return redirect('post_detail', pk=comment.post.pk)
