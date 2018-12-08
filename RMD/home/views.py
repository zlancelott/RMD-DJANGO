from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import UploadFileForm

from .models import User, Subject, SubjectClass, Lesson, LessonFile

from django.http import HttpResponseRedirect

@login_required
def home(request):
    user_logged_in = request.user

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()

    # Turmas em que o usuário está moderando
    subjects_moderates = user_logged_in.moderador.all()

    for subject_moderate in subjects_moderates:
        if subject_moderate.is_mod:
            moderador = subject_moderate.is_mod

    json_data = {
        #Turmas
        'subject_classes':list(subject_classes),
        'moderador': moderador
    }
    return render(request, 'home.html', json_data)


def logout_view(request):
    logout(request)
    return redirect ('home')

@login_required
def submeter_arquivos(request):
    user_logged_in = request.user

    # Variável para mostrar o botão de moderador
    moderador = user_logged_in.moderador.all()[0].is_mod

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()

    if request.method == "POST":
        form = UploadFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UploadFileForm()
        form.fields['subject'].initial = 1
        form.fields['lesson'].initial = 1


        ######### PRECISA MELHORAR ###########
        form.fields['author'].initial = 1
    
    json_data = {
        #Turmas
        'subject_classes':list(subject_classes),
        'form': form,
        'moderador': moderador,
    }

    return render(request, 'submeter_arquivos.html', json_data)

@login_required
def show_image(request):
    return render(request, 'show_images.html')

def check_is_moderator(user):
    return user.moderador.all()[0].is_mod

# Apenas moderadores podem acessar esta página
@user_passes_test(check_is_moderator)
def evaluate_submissions(request):
    user_logged_in = request.user
    
    # Variável para mostrar o botão de moderador
    moderador = user_logged_in.moderador.all()[0].is_mod

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()

    # Turmas moderadas
    subject_classes_moderate = [i.subject_class_id for i in user_logged_in.moderador.all()]

    lessons = []

    for subject_class in subject_classes_moderate:
        # Obtendo Aulas dessa disciplina
        lessons.append(subject_class.lessons.all())

    lessons_files = []
    for lesson_x in lessons:
        for lesson_y in lesson_x:
            lessons_files.append(lesson_y.lesson.all().filter(evaluated=False))

    new_lesson_files = []

    for query in lessons_files:
        for lesson in query:
            new_lesson_files.append(lesson)

    print (lessons)

    json_data = {
        'subject_classes':list(subject_classes),
        'moderador': moderador,
        'lessons_files': new_lesson_files
    }

    return render(request, 'evaluate_submissions.html', json_data)

# Apenas moderadores podem acessar esta página
@user_passes_test(check_is_moderator)
def submission_details(request, lesson_file_id):
    user_logged_in = request.user
    
    # Variável para mostrar o botão de moderador
    moderador = user_logged_in.moderador.all()[0].is_mod

    # Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()

    lesson_file = get_object_or_404(LessonFile, id=lesson_file_id)

    if request.method == "POST":
        form = UploadFileForm(request.POST or None, request.FILES or None, instance = lesson_file)

        if form.is_valid():
            # Se aceitar a submissão ele muda o valor do evaluated para True
            # e salva o objeto
            if 'btn_aceitar' in request.POST:
                lesson_file.evaluated = True
                lesson_file.save()
                form.save()
                return redirect('home')

            # Se rejeitar a submissão ele deleta o arquivo
            if 'btn_rejeitar'in request.POST:
                lesson_file.delete()
                return redirect('home')
                

    else:
        form = UploadFileForm(instance = lesson_file)

    json_data = {
        'subject_classes':list(subject_classes),
        'moderador': moderador,
        'lesson': lesson_file,
        'form': form
    }

    return render(request, 'submission_details.html', json_data)