from django.db import models
from django.contrib.auth.models import User
import datetime
from cloudinary import CloudinaryField
# Create your models here.

class Profile (models.Model):
    profile_photo=CloudinaryField('profile_photo')
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
class Image(models.Model):
    image=CloudinaryField('image')
    image_name = models.CharField(max_length=255)
    caption = models.CharField(max_length=60)
    pub_date = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes',blank=True)
    user = models.ForeignKey(on_delete=models.CASCADE)
    
    class Meta:
        ''' class method to display images by published date'''
        ordering = ['pub_date']
    def __str__(self):
        return f'{self.image_name}'