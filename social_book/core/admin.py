from django.contrib import admin
from .models import  Post , Users , LikePost,Follow ,CommentPost,Chats

# Register your models here.
admin.site.register(Post)
admin.site.register(Users)
admin.site.register(LikePost)
admin.site.register(Follow)
admin.site.register(CommentPost)
admin.site.register(Chats)