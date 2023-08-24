from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True ,unique=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    location = models.CharField(max_length=100,blank=True)
    avatar = models.ImageField(null=True,default="avatar.png")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    