from django import forms
from django.contrib.auth.models import User
from MAINAPP.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username', 'email' , 'password')

class ContactMessageForm(forms.ModelForm):
    class Meta():
        model =  ContactMessage
        fields =('reviewer_name','reviewer_email','reviewer_message',)

class SubscriberForm(forms.ModelForm):
    class Meta():
        model =  Subscriber
        fields =('subscriber_name','subscriber_email',)
