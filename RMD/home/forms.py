from django.forms import ModelForm
from .models import LessonFile

class UploadFileForm(ModelForm):
    class Meta:
        model = LessonFile

        fields = ['name', 'subject', 'lesson', 'author', 'file_image']
