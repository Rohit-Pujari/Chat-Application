from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=500,null=True,blank=True)
    picture = models.ImageField(upload_to='media/UserProfile/')
    
    def __str__(self):
        return self.name + self.picture