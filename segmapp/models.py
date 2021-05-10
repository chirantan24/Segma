from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    writer=models.ForeignKey(User,null=True,on_delete=models.CASCADE);
    title=models.CharField(max_length=2000,null=True);
    text=models.CharField(max_length=10000);
    time_created=models.DateTimeField(null=True);
    image=models.ImageField(upload_to='pics/',blank=True,null=True);
# Create your models here.

class Comment(models.Model):

    commenter=models.ForeignKey(User,null=True,on_delete=models.CASCADE);
    post=models.ForeignKey(Post,related_name='comments',null=True,on_delete=models.CASCADE);
    time_created=models.DateTimeField(null=True);
    text=models.CharField(max_length=10000);
    class Meta:
        ordering=['-time_created']
class Relation(models.Model):
    follower=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE);
    following=models.ForeignKey(User,on_delete=models.CASCADE);
    class Meta:
        unique_together=[
        'follower','following'
        ]
class Request(models.Model):
    by=models.ForeignKey(User,related_name='req',on_delete=models.CASCADE);
    to=models.ForeignKey(User,on_delete=models.CASCADE);

class Bio(models.Model):
    user=models.OneToOneField(User,related_name='bio',on_delete=models.CASCADE,primary_key=True);
    profile_pic=models.ImageField(upload_to='profile_pics/',blank=True,null=True);
    text=models.CharField(max_length=10000)
