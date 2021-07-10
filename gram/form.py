from django import forms
from django.contrib.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Image,Comments

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields['username','email','password1','password2']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields['username','email']
        
class ProfileUpdate(forms.ModelForm):
    class Meta:
     model=Profile
     fields = ['profile_photo']  

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','image_name','caption'] 
        
    def form_valid(self,form):
        form.instance.user = self.request.profile 
        return super().form_valid(form)
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fileds = ['username','email']
        
class CommentsForm(forms.ModelForm):
    class Meta:
        models= Comments
        fields  = ['comment'] 