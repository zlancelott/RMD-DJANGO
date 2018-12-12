from django import forms
from .models import LessonFile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = LessonFile

        fields = ['name', 'subject', 'lesson','author', 'file_image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'alt': 'Campo Nome'
            }),

            'subject': forms.Select(attrs={
                'class': 'form-control',
                'alt': 'Campo Disciplina',
            }),

            'lesson': forms.Select(attrs={
                'class': 'form-control',
                'alt': 'Campo Aula'
            })
        }

        labels = {
            'name': 'Nome',
            'subject': 'Disciplina',
            'lesson': 'Aula',
            'file_image': 'Arquivos'
        }



class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')