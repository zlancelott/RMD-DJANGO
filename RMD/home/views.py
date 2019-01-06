from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import SubForm, UpdateSubForm

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

            return redirect ('home')


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
        'submissions': user_logged_in.submissions.filter(approved=True), #Apenas submissões já aprovadas
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
    try:
        moderador = ModerationOfSubjects.objects.get(pk=user.id)
        print (moderador)
    except ModerationOfSubjects.DoesNotExist:
        moderador = False
        print ("Não existe")

    return moderador

# Apenas moderadores podem acessar esta página
@user_passes_test(check_is_moderator)
def evaluate_submissions(request):
    user_logged_in = request.user
    
    try:
        moderador = ModerationOfSubjects.objects.get(pk=user_logged_in.id)
        print (moderador)
    except ModerationOfSubjects.DoesNotExist:
        moderador = False
    
    json_data = {
        # Submissões da discipliuna do moderador e que ainda não foram aprovadas
        'submissions': (user_logged_in.submissions.filter(subject = moderador.subject)).filter(approved=False),
        'moderador': moderador,
        }

    return render(request, 'evaluate_submissions.html', json_data)

# Apenas moderadores podem acessar esta página
@user_passes_test(check_is_moderator)
def submission_details(request, submission_id):
    user_logged_in = request.user

    try:
        moderador = ModerationOfSubjects.objects.get(pk=user_logged_in.id)
        print (moderador)
    except ModerationOfSubjects.DoesNotExist:
        moderador = False

    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == "POST":
        form = UpdateSubForm(request.POST or None, request.FILES or None)
    
        if form.is_valid():
            # Se aceitar a submissão ele muda o valor do approved para True
            # e salva o objeto
            if 'btn_aceitar' in request.POST:
                print ("Estou entrando")
                # Salvando Submissão
                submission.subject = form.cleaned_data['subject']
                submission.submission_date = form.cleaned_data['class_date']
                submission.description = form.cleaned_data['description']
                submission.topic = form.cleaned_data['topic']
                submission.uploader = user_logged_in
                submission.approved = True
                
                submission.save()

                return redirect('home')

            # Se rejeitar a submissão ele deleta o arquivo
            if 'btn_rejeitar'in request.POST:
                submission.delete()
                return redirect('home')
                

    else: # O que vai ser mostrado ao entrar na página  
        form = UpdateSubForm()

        form.fields['subject'].initial = submission.subject
        form.fields['topic'].initial = submission.topic
        form.fields['class_date'].default = '03/12/1996'
        form.fields['description'].initial = submission.description


    json_data = {
        'moderador': moderador,
        'form': form,
        'files': submission.files.all(),
    }

    return render(request, 'submission_details.html', json_data)