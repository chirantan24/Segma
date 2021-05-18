from django import forms

from django.contrib.auth.models import User
from segmapp import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserCreateForm(UserCreationForm):
    class Meta:
        fields =('first_name','last_name','username','email','password1','password2')
        model = User
class PostEditForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields=('title','text','file')
        widgets={
        'text': forms.Textarea(attrs={"cols":50}),
        # 'image': PictureWidget
        }
        labels={
        'text':'',
        'image':''
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields=('text',)
        widgets={
        'text': forms.Textarea(attrs={"cols":50,"rows":5}),
        }
        labels={
        'text':''
        }
class BioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].required = True
    class Meta:
        model = models.Bio
        fields=('text','profile_pic')
        widgets={
        'text': forms.Textarea(attrs={"cols":50,"rows":5,"placeholder":'Enter your Bio information here.'}),
        }
        labels={
        'text':'',
        'profile_pic':'Upload Profile pic'
        }
