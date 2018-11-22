from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm

from django.http import HttpResponseRedirect

@login_required
def home(request):
    info = {
        'disciplinas':[{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}],
        'aulas': [{"id": "1", "nome": "Aula 1"}, {"id": "2", "nome": 'Aula 2'},
                {"id": "3", "nome": "Aula 3"}, {"id": "4", "nome": "Aula 4"}]
    }

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