from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm

from .models import User, Subject, SubjectClass, Lesson

from django.http import HttpResponseRedirect

@login_required
def home(request):
    user_logged_in = request.user

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()


    json_data = {
        #Turmas
        'subject_classes':list(subject_classes),
    }


    return render(request, 'home.html', json_data)


def logout_view(request):
    logout(request)
    return redirect ('home')


def submeter_arquivos(request):
    user_logged_in = request.user

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()

    if request.method == "POST":
        form = UploadFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():

            ### ERRADO ###
            form.fields['author'] = request.user.id
            form.save()
            return redirect('home')

    else:
        form = UploadFileForm()

    
    json_data = {
        #Turmas
        'subject_classes':list(subject_classes),
        'form': form
    }

    return render(request, 'submeter_arquivos.html', json_data)

def show_image(request):
    return render(request, 'show_images.html')