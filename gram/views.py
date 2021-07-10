from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import request,HttpResponse,Http404
from django.contrib import messages
import pdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Image,Profile,Comments,Follow
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
    
    context={'photos':photos[::-1],'p_form':p_form,'u_form':u_form}
    
    return render(request,'registration/profile.html',context)

def image(request,image_id):
    try:
        image=Image.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    
    return render(request, 'image.html',{'image':image})

def search_results(request):
    if 'pic' in requset.GET and request.GET['pic']:
        search_terms = request.GET.get('pic')
        searched_images = Image.search_by_name(search_term)
        message = f'search_term'
        context={'message':message,'image':searched_images}
        
        return render(request, 'search.html',context)
    else:
        message=f"You haven't searched for any term"
        return render(request,'search.html',{'message':message})   


def post(request,image_id):
    image = Image.objects.get(id=image_id)
    comments = Comments.objects.all()
    commentform = CommentsForm()
    if request.method == 'POST':
        commentform=CommentsForm(request.POST)
        if commentform.is_valid():
            content = commentform.fields['comment']
            new_comment=Comments(comment=content,image=image,user=request.user)
            new_comment.save()
            
            context={
                'new_comment':new_comment
            }
            return redirect('home',context)
    
    context = {
        
        'commentform':commentform,
        'image':image,
        'comments':comments
    }
    
    return render(request,'comment.html',context)

def follow (request,to_follow):
    if request.Method =='GET':
        user_profile3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile,followed=user_profile3)
        follow_s.save()
        return redirect('user_profile',user_profile3.user.username)
    
def unfollow (request,to_unfollow):
    if request.method =="GET":
        user_profile2 = Profile.object.get(pk = to_unfollow)
        unfollow_d = Follow.objects.filter(follower = request.user.profile,followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile',user_profile2.user.username)
    
@login_required
def home(request):
    photos = Image.objects.all()
    profile = Profile.objects.all()
    form = ImageForm()
    users = User.objects.all()
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {
        'photos': photos,
        'form':form,
        'profile':profile,
        'users':users
    }
    return render(request, 'home.html', context)

@login_required
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_images = user_prof.profile.images.all()
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_images': user_images,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'users/user_profile.html', params)


@login_required
def index(request):
    images = Image.objects.all()
    comments = Comment.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit = False)
            image.user = request.user.profile
            image.save()
            messages.success(request, f'Successfully uploaded your pic!')
            return redirect('index')
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {"images":images[::-1], "form": form, "users": users, "comments": comments })
