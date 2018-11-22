from django.contrib import admin

from .models import User, UserClassAssociation, Course, Subject, SubjectClass, Topic, Lesson, LessonFile

# Register your models here.
admin.site.register(User)
admin.site.register(UserClassAssociation)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(SubjectClass)
admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(LessonFile)
