from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login, logout
from .models import Post , User ,LikePost
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_profile = User.objects.get(id=request.user.id)
    posts = Post.objects.all().order_by('-created_at')
    likes = LikePost.objects.all()
    context = {
        'user_profile':user_profile,
        'posts': posts,
        'likes': likes,

    }
    return render(request,'index.html',context)

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')

def like_post(request,pk):
    user = request.user 
    post = Post.objects.get(id=pk) 
    like_filter = LikePost.objects.filter(post=post,user=user).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post=post,user=user)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('index')

def profile(request,pk):
    user_id = User.objects.get(id=pk)
    user_posts = Post.objects.filter(user__id=pk)
    likes = LikePost.objects.all()
    context = {
        'user_id':user_id,
        'user_posts':user_posts,
        'likes':likes
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def settings(request):
    user_profile = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            backgroundImage = request.FILES.get('backgroundImage')
            image = user_profile.avatar
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.backgroundImage = backgroundImage
            user_profile.avatar = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:

            backgroundImage = user_profile.backgroundImage
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.backgroundImage = backgroundImage
            user_profile.avatar = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('settings')
    content = { 
        'user_profile': user_profile
    }
    return render(request,'settings.html',content)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                return redirect('signup')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request,'signin.html')

@login_required(login_url='signin')
def Logout(request):
    logout(request)
    return redirect('signin')