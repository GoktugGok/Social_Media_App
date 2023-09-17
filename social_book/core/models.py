from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractUser


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

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

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
    
    

    