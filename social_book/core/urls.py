from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('settings', views.settings, name="settings"),
    path('upload', views.upload, name="upload"),
    path('profile', views.profile, name="profile"),
    path('like-post/<str:pk>',views.like_post,name="like-post"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('logout',views.Logout,name="logout"),
]
