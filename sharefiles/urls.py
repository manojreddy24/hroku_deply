from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
   # path('post_msg', views.post_msg, name='post_msg'),
    path('view_group', views.view_group, name='home'),
   # path('view_my_posts', views.view_my_posts, name='view_my_posts'),
    path('badreq', views.view_badreq, name='badreq'),
    path('<str:room>/', views.room, name='home'),
    path('check_group_auth', views.check_group_auth, name='check_group_auth'),
    path('send', views.send, name='send'),
    path('getMessages/<str:group>/', views.messagebox, name='getMessages'),

   

  

]
