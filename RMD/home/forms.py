from django.forms import ModelForm
from .models import LessonFile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UploadFileForm(ModelForm):
    class Meta:
        model = LessonFile

        fields = ['name', 'subject', 'lesson', 'author', 'file_image']



class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')