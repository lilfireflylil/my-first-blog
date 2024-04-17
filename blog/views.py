from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    # post = Post.objects.get(pk=pk)      ## this code will throw query error if the pk does not exist
    post = get_object_or_404(Post, pk=pk) # the code will throw page not found if the pk does not exist. will display much nicer page.
    return render(request, 'blog/post_detail.html', {'post': post})
