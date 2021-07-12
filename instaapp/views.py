from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ImageUploadForm, CommentForm
from .models import Profile, Image, User, Subscribers, Follow, Comment, Like
from cloudinary.forms import cl_init_js_callbacks
from django.core.exceptions import ObjectDoesNotExist
# from .email import send_welcome_email

@login_required
def index(request):
    images = Image.objects.all()
    comments = Comment.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit = False)
            image.user = request.user.profile
            image.save()
            messages.success(request, f'Successfully uploaded your pic!')
            return redirect('index')
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {"images":images[::-1], "form": form, "users": users, "comments": comments })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data['email']
            recipient = Subscribers(name = username,email =email)
            recipient.save()
            # send_welcome_email(username,email)
            messages.success(request, f'Successfully created account created for {username}! Please log in to continue')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    images = request.user.profile.images.all()
    comments = Comment.objects.all()
    return render(request, 'users/profile.html', {"images":images[::-1], "comments": comments})

@login_required
def update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
        instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Successfully updated your account!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/update.html', context)

def image(request,image_id):
    try:
        image = Image.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"image.html", {"image":image})

@login_required
def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_profile(search_term)
        message = f"{search_term}"
        return render(request, 'search.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'search.html', {'message': message})

def like_post(request):
    user = request.user
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        img_obj = Image.objects.get(id = image_id)
        if user in img_obj.liked.all():
            img_obj.liked.remove(user)
        else:
            img_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user = user, image_id = image_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect(request, 'index.html')

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

def follow(request, to_follow):
    if request.method == 'GET':
        user_profile3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_profile3)
        follow_s.save()
        return redirect('user_profile', user_profile3.user.username)

def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)

@login_required 
def comment(request,image_id):
        current_user=request.user
        image = Image.objects.get(id=image_id)
        user_profile = User.objects.get(username=current_user.username)
        comments = Comment.objects.all()
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.image = image
                        comment.user = request.user
                        comment.save()  
                return redirect('index')
        else:
                form = CommentForm()
        return render(request, 'comment.html',locals())
