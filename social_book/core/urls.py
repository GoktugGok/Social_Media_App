<<<<<<< HEAD
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('settings', views.settings, name="settings"),

    path('upload', views.upload, name="upload"),

    path('profile/<str:pk>', views.profile, name="profile"),

    path('search', views.search, name="search"),

    path('like-post/<str:pk>',views.like_post,name="like-post"),

    path('comment/<str:pk>',views.comment,name="comment"),
    path('comment-delete/<int:pk>/', views.comment_delete, name='comment-delete'),

    path('post-delete/<str:pk>',views.post_delete,name="post-delete"),
    path('follow/<str:pk>/',views.follow,name="follow"),

    path('chat',views.chat,name="chat"),
    path('chat-user/<str:pk>',views.chat_user,name="chat-user"),

    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('logout',views.Logout,name="logout"),
]
=======
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('settings', views.settings, name="settings"),
    path('upload', views.upload, name="upload"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('like-post/<str:pk>',views.like_post,name="like-post"),
    path('comment',views.comment,name="comment"),
    path('comment-delete/<str:pk>',views.comment_delete,name="comment-delete"),
    path('post-delete/<str:pk>',views.post_delete,name="post-delete"),
    path('follow/<str:pk>/',views.follow,name="follow"),
    path('chat',views.chat,name="chat"),
    path('chat-user/<str:pk>',views.chat_user,name="chat-user"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('logout',views.Logout,name="logout"),
]
>>>>>>> 823c6c51c73bd61132b45e44cb92c99056ee98d3
