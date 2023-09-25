from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth import authenticate , login, logout
from django.db.models import Q
from .models import Post , Users ,LikePost ,Follow, CommentPost, Chats
from django.contrib.auth.decorators import login_required
from uuid import UUID
from django.contrib import messages
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_profile = Users.objects.get(id=request.user.id)

    # Mevcut kullanıcının takip ettiği kullanıcıları alın
    takip_ettiklerim = Follow.objects.filter(following=request.user).values_list('followed', flat=True)
    takip_ettiklerim_kullanicilar = Users.objects.filter(id__in=takip_ettiklerim)


    tum_kullanicilar = Users.objects.exclude(id=request.user.id)
    
    takip_etmediklerim = []

    for kullanici in tum_kullanicilar:
        if kullanici not in takip_ettiklerim_kullanicilar:
            takipci_sayisi = Follow.objects.filter(followed=kullanici).count()
            takip_etmediklerim.append({'kullanici': kullanici, 'takipci_sayisi': takipci_sayisi})

    posts = Post.objects.all().order_by('-created_at')
    likes = LikePost.objects.all()
    context = {
        'user_profile':user_profile,
        'takip_etmediklerim':takip_etmediklerim,
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

def comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post')
        user = request.user
        comment = request.POST['comment'].strip()

        if comment:
            post = Post.objects.get(id=post_id)
            new_comment = CommentPost.objects.create(post=post, user=user, comment=comment)
            new_comment.save()
            return redirect('index')
    else:
        return redirect('index')
    
def comment_delete(request,pk):
    comment_id = CommentPost.objects.get(id=pk)

    if comment_id:
        comment_id.delete()
        return redirect('index')

def post_delete(request,pk):
    post_id = Post.objects.get(id=pk)

    if post_id:
        post_id.delete()
        return redirect('index')

@login_required(login_url='signin')
def like_post(request,pk):
    user = request.user 
    post = Post.objects.get(id=pk) 
    like_filter = LikePost.objects.filter(post=post,user=user).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post=post,user=user)
        new_like.save()
        post.people_who_liked.add(user)
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.people_who_liked.remove(user)
        post.save()
        return redirect('index')

@login_required(login_url='signin')
def follow(request, pk):
    user_to_follow = get_object_or_404(Users, pk=pk)
    user_profile = request.user

    if user_profile != user_to_follow: 
        follow_instance, created = Follow.objects.get_or_create(following=user_profile)

        if follow_instance.is_following(user_to_follow):
            follow_instance.followed.remove(user_to_follow)
        else:
            follow_instance.followed.add(user_to_follow)


    return redirect('profile',user_to_follow.id)

@login_required(login_url='signin')
def chat(request):
    user_profile = request.user

    takip_ettiklerim = Follow.objects.filter(following=request.user).values_list('followed', flat=True)
    takip_ettiklerim_kullanicilar = Users.objects.filter(id__in=takip_ettiklerim)

    context = {
        'user_profile':user_profile,
        'takip_ettiklerim_kullanicilar':takip_ettiklerim_kullanicilar,
    }
    return render(request,'chat.html',context)

@login_required(login_url='signin')
def chat_user(request,pk):
    user_profile = request.user
    chat_user = Users.objects.get(id=pk)

    chats = Chats.objects.filter(Q(user1=request.user, user2=chat_user) | Q(user1=chat_user, user2=request.user)).order_by('created')

    
    if request.method == 'POST':
        firstUser = request.user
        lastUser = chat_user
        chat = request.POST['chat']

        new_chat = Chats.objects.create(user1=firstUser,user2=lastUser,chat=chat)
        new_chat.save()
        return redirect('chat-user', pk )

    context = {
        'user_profile':user_profile,
        'chat_user':chat_user,
        'chats':chats
    }
    return render(request,'chat-user.html',context)

@login_required(login_url='signin')
def profile(request,pk):
    user_id = Users.objects.get(id=pk)
    user_posts = Post.objects.filter(user__id=pk).order_by("-created_at")
    likes = LikePost.objects.all()

    takip_ettiklerim = Follow.objects.filter(following=request.user).values_list('followed', flat=True)
    takip_ettiklerim_kullanicilar = Users.objects.filter(id__in=takip_ettiklerim)
    print(user_id,'asdad')
    print(takip_ettiklerim_kullanicilar)
    if user_id in takip_ettiklerim_kullanicilar:
        print('sadas')
    # takip eden kişilerin sayısı
    followed_count = user_id.followed.all().count()

    
    # takip edip etmediğini kontrol ediyor
    follow_filter = Follow.objects.filter(followed=user_id,following=request.user).first()

    # takip ettiklerinin sayısı
    following_counts = Follow.objects.filter(following=user_id).first()
    if following_counts == None:
        following_count = 0
    else:
        following_count = following_counts.followed.count()

    context = {
        'user_id':user_id,
        'follow_filter':follow_filter,
        'followed_count':followed_count,
        'following_count':following_count,
        'takip_ettiklerim_kullanicilar':takip_ettiklerim_kullanicilar,
        'user_posts':user_posts,
        'likes':likes
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user_profile = Users.objects.get(id=request.user.id)
    users_filter = Users.objects.all().filter(Q(username__icontains  = q)|
                                      Q(id__icontains  = q)
                                      )
    context = {
        'user_profile':user_profile,
        'users_filter':users_filter,
    }
    return render(request,'search.html',context)

@login_required(login_url='signin')
def settings(request):
    user_profile = Users.objects.get(id=request.user.id)
    if request.method == 'POST':
        print()
        if request.FILES.get('image') == None:
            if request.FILES.get('backgroundImage') == None:
                backgroundImage = user_profile.backgroundImage
            else:
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
            if request.FILES.get('backgroundImage') == None:
                backgroundImage = user_profile.backgroundImage
            else:
                backgroundImage = request.FILES.get('backgroundImage')
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
            if Users.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            
            elif Users.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = Users.objects.create_user(username=username,email=email,password=password)
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


def Logout(request):
    logout(request)
    return redirect('signin')