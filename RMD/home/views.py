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


    ###### OBTENDO LESSONS / AULAS ######
    ###### SubjectClass.lessons.all() ######

    info = {
        'subjects':[i.subject for i in subject_classes], #Compreensão de lista para obter as disciplinas das turmas
        'aulas': [{"id": "1", "nome": "Aula 1"}, {"id": "2", "nome": 'Aula 2'},
                {"id": "3", "nome": "Aula 3"}, {"id": "4", "nome": "Aula 4"}]
    }

    print (info, "\n\n\n\n")

    return render(request, 'home.html', info)


def logout_view(request):
    logout(request)
    return redirect ('home')


def submeter_arquivos(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UploadFileForm()
        return render(request, 'submeter_arquivos.html', {'form': form})