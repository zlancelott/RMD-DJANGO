from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Submission, File, User, Subject



class SubForm(forms.Form):
    ### CRIAR FORMULÁRIO ###
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    topic = forms.CharField(max_length=100)
    class_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(max_length=250)
    files = forms.ImageField(widget=forms.FileInput(attrs={'multiple':True}))

