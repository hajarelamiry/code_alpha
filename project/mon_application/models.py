from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

user=get_user_model()

# Create your models here.
class profile(models.Model):
    user=models.ForeignKey(user, on_delete=models.CASCADE)
    id_user=models.IntegerField()
    bio=models.TextField(blank=True)
    profileimg=models.ImageField(upload_to='profile_image',default='avatar-3814049_1280.png')
    location=models.CharField(max_length=100,blank=True)
    
class post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_images',default="avatar-3814049_1280.png")
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)


class like(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)
    
class followers(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)