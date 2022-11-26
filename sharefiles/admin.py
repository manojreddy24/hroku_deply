from django.contrib import admin

from .models import Group, LikePost, Message, Post

# Register your models here.
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(LikePost)
admin.site.register(Post)