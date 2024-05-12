from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    # The related_name option in models.ForeignKey allows us to have 
    # access to comments from within the Post model.
    
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # I want only registered user can comment and there comment be posted without
    # waiting for blog's admin approval. and then only the author of the comment and
    # admin of the blog can delete the comment. so I am just leaving this function 
    # alone cause it is taught in the tutorial. 
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self) -> str:
        return self.text

