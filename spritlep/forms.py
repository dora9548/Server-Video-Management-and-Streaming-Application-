from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Video
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'video_file']


