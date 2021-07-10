from django.db import models
from django.contrib.auth.models import User
import datetime
from cloudinary.models import CloudinaryField
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        ''' class method to display images by published date'''
        ordering = ['pub_date']
    def __str__(self):
        return f'{self.image_name}'
    
class Comments(models.Model):
    comment = models.CharField(max_length=300)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateField(null=True,auto_now_add=True)
    
    def __str__(self):
        return self.comment
    
LIKE_CHOICES =(('Like','Like'),('Unlike','Unlike'))

class Like(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=10,null=True,default='Like',choices = LIKE_CHOICES)
    
    def __str__(self):
        return self.image
    
class Follow(models.Model):
    follower=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='following')
    followed = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='followers')
    
    def __str__(self):
        return f'{self.follower} Follow'