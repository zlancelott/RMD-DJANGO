from django.shortcuts import render

# Create your views here.
def disciplina(request, disciplina):
    # # Conexão FTP
    # ftp = FTP('192.168.15.5')
    # ftp.login(user='FTP_Server', passwd='ftpserver')

    # # disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
    # #                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    # # Acessando a pasta no servidor correspondente as aulas da disciplina
    # path_lessons = "/Computer Science/7-semester/%s/" % (disciplina)
    # ftp.cwd(path_lessons)
    # lessons = ftp.nlst()  # Listando as aulas da disciplina

    # aulas = []
    # for j in range(len(lessons)):
    #     aulas.append({})
    #     aulas[j]["id"] = j
    #     aulas[j]["nome"] = lessons[j]

    json_info = {
        'disciplinas':[{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}],
        'aulas': [{"id": "1", "nome": "Aula 1"}, {"id": "2", "nome": 'Aula 2'},
                {"id": "3", "nome": "Aula 3"}, {"id": "4", "nome": "Aula 4"}],
        'title': disciplina
    }


    return render(request, 'aulas.html', json_info)