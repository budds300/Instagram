from django.contrib import admin
from .models import Profile, Image, Like, Subscribers, Comment, Follow

# Register your models here.
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Subscribers)
admin.site.register(Comment)
admin.site.register(Follow)

