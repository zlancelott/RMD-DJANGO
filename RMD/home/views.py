from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import SubForm

from .models import User, Subject, Submission, File, ModerationOfSubjects

from django.http import HttpResponseRedirect

@login_required
def home(request):
    user_logged_in = request.user

    try:
        moderador = ModerationOfSubjects.objects.get(pk=user_logged_in.id)
        print (moderador)
    except ModerationOfSubjects.DoesNotExist:
        moderador = False
        print ("Não existe")


    # Obtendo Formulário 
    if request.method == "POST":
        form = SubForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            # Salvando Submissão
            submission = Submission()
            submission.subject = form.cleaned_data['subject']
            submission.submission_date = form.cleaned_data['class_date']
            submission.description = form.cleaned_data['description']
            submission.topic = form.cleaned_data['topic']
            submission.uploader = user_logged_in

            submission.save()

            # Salvando Arquivo (s)

            for image in request.FILES.getlist('files'):
                file = File()
                file.file_image = image
                file.submission = submission

                file.save()


    else:
        form = SubForm(request.POST or None, request.FILES or None)

        # Editando as Labels
        form.fields['subject'].label = 'Disciplina'
        form.fields['topic'].label = 'Assunto'
        form.fields['class_date'].label = 'Data da Aula'
        form.fields['description'].label = 'Descrição'
        form.fields['files'].label = 'Imagens da Aula'
        


    json_data = {
        'submission_form' : form, #Formulário para Submissão
        'submissions': user_logged_in.submissions.all(), #Submissões
        'moderador': moderador,
        }

    return render(request, 'home.html', json_data)


def logout_view(request):
    logout(request)
    return redirect ('home')
    
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