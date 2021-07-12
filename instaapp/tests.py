from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Image, Comment

class ProfileClassTest(TestCase):
    def setUp(self):
        self.new_user = User(username='montez', email='montez@gmail.com', password='qwer')
        self.new_profile = Profile(profile_photo='', bio='ontriptic', user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_method(self):
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
    
class ImageClassTest(TestCase):
    def setUp(self):
        self.new_user = User(username='montez', email='montez@gmail.com', password='qwer')
        self.new_image = Image( gallery_image='',image_name='one', image_caption='chasing sunsets be like', user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))

    def test_save_image(self):
        image = Image.objects.all()
        self.assertTrue(len(image)>0)

class CommentsTest(TestCase):
    def setUp(self):
        self.new_user = User(username='montez', email='montez@gmail.com', password='qwer')
        self.new_image = Image(user='montez', image='', caption='ontriptic', profile=self.new_user)
        self.new_comment = Comment(comment='tembeaKenya',image=self.new_image,user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        comment = Comment.objects.all()
        self.assertTrue(len(comment)>0)
