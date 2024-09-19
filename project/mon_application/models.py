from django.db import models
from django.contrib.auth import get_user_model

user=get_user_model()

# Create your models here.
class profile(models.Model):
    user=models.ForeignKey(user, on_delete=models.CASCADE)
    id_user=models.IntegerField()
    bio=models.TextField(blank=True)
    profileimg=models.ImageField(upload_to='profile_image',default='avatar-3814049_1280.png')
    location=models.CharField(max_length=100,blank=True)
    
