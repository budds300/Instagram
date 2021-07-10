from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import request,HttpResponse,Http404
from django.contrib import messages
import pdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Image,Profile,Comments
import datetime as dt
from .form import UserCreationForm,UserRegistrationForm,UserUpdateForm,ProfileUpdate,CommentsForm,ImageForm
from django.core.exceptions import ValidationError,ObjectDoesNotExist

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data['email']
            message.success(request, f'Your account has been created! You are now able to login')
            return redirect('home')
        
    else :
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'registration.tml',context)

@login_required
def profile(request):
    photos = Image.objects.all()
    profile_info=Profile.objects.all()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance= request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            message.success(request,f'Your account has been updated')
            return redirect('profile')
        
    else: 
        u_form = UserUpdateForm(instance=request.user)
        p_form=ProfileUpdate(instance=request.user.profile)
    
    context={'photos':photos,'p_form':p_form,'u_form':u_form}
    
    return render(request,'registration/profile.html',context)

def image(request,image_id):
    try:
        image=Image.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
            
