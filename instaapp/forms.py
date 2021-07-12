from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Image, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [ 'image_name', 'image_caption','gallery_image' ]

    def form_valid(self, form):
        form.instance.user = self.request.profile
        return super().form_valid(form)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['image','user']

    class Meta:
        model = Comment
        fields = ('comment',)
  