from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
from PIL import Image
import cloudinary
import datetime as dt

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    bio = models.TextField()
    profile_photo = CloudinaryField('profile_photo')


    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_bio(cls,id, bio):
        update_profile = cls.objects.filter(id = id).update(bio = bio)
        return update_profile
    
    @classmethod
    def search_profile(cls, search_term):
        profs = cls.objects.filter(user__username__icontains=search_term)
        return profs

    def __str__(self):
        return f'{self.user.username} Profile'

class Image(models.Model):
    gallery_image = CloudinaryField('gallery_image', null=True)
    image_name = models.CharField(max_length =30, null=True)
    image_caption = models.CharField(max_length =70, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    liked = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images', null=True)

    class Meta:
        '''
        Class method to display images by date published
        '''
        ordering = ['pub_date']

    def save_image(self):
        '''
        Method to save our images
        '''
        self.save()

    def delete_image(self):
        '''
        Method to delete our images
        '''
        self.delete()

    @property
    def num_liked(self):
        return self.liked.all().count()

    @classmethod
    def update_caption(cls, self, caption):
        update_cap = cls.objects.filter(id = id).update(caption = caption)
        return update_cap

    def __str__(self):
        return self.image_name

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null = True)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10, null = True)

    def __str__(self):
        return self.image

class Subscribers(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments(cls,id):
        comments = cls.objects.filter(image__id=id)
        return comments

    def __str__(self):
        return self.comment

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'