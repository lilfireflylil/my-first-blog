from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Post, Comment


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder': '*********'}))
    # widgets variable does not work. 
    # maybe because this LoginForm is not inheriting from a ModelForm.
    # ChatGPT helped me for this :D 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
        labels = {'text': 'Description'}
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'Post title here :)'})
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Comment'} # it is just for display 
        widgets = {
            'text': forms.Textarea(attrs={'autofocus': 'autofocus', 'placeholder': 'Write some positive comment! :)'})
        }