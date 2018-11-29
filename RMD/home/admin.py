from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from .models import User, UserClassAssociation, Course, Subject, SubjectClass, Topic, Lesson, LessonFile
from .forms import UserCreationForm, UserChangeForm

# Register your models here.


class UserAdmin2(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username',]

admin.site.register(User, UserAdmin2)
admin.site.register(UserClassAssociation)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(SubjectClass)
admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(LessonFile)


