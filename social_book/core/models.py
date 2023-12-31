from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Users(AbstractUser):
    username = models.CharField(max_length=200, null=True ,unique=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True,default="Bio...")
    location = models.CharField(max_length=100,blank=True)
    avatar = models.ImageField(upload_to="profile_images", null=True,default="avatar.png")
    backgroundImage = models.ImageField(upload_to="background", null=True,default="windows-xp-wallpaper-bliss_T5gheWz.jpg")
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def follower_count(self):
        return self.followers.count()
    
class CommentPost(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.user.username
    
class Chats(models.Model):
    user1 = models.ForeignKey(Users, related_name='chat_user1' ,on_delete=models.CASCADE)
    user2 = models.ForeignKey(Users, related_name='chat_user2', on_delete=models.CASCADE)
    chat = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.user1.username
    
class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    people_who_liked = models.ManyToManyField(Users,related_name='People_who_liked',blank=True)
    comments = models.ManyToManyField(CommentPost, related_name='comments', blank=True)

    #no_of_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.user.username
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username
     
class Follow(models.Model):
    following = models.OneToOneField(Users, related_name='following',on_delete=models.CASCADE)
    followed = models.ManyToManyField(Users,related_name='followed',blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.following.username
    
    def is_following(self, user_to_check):
        return self.followed.filter(id=user_to_check.id).exists()
    
    

    