from django.shortcuts import render

def disciplina(request, disciplina):
    user_logged_in = request.user

    info2 = {'disciplinas':[], 'aulas':[]}

    #Turmas em que o usuário está matriculado
    subject_classes = user_logged_in.subjectclasses.all()


    json_info = {
        # Obtendo as disciplinas apartir das turmas
        'subjects': [i.subject for i in subject_classes],
        'aulas': [{"id": "1", "nome": "Aula 1"}, {"id": "2", "nome": 'Aula 2'},
                {"id": "3", "nome": "Aula 3"}, {"id": "4", "nome": "Aula 4"}],
        'title': disciplina
    }


    return render(request, 'aulas.html', json_info)