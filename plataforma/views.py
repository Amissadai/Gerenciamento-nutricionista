from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DadosPaciente, Pacientes
from django.contrib import messages
from django.contrib.messages import constants


@login_required(login_url='/auth/login/')
def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes':pacientes})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if len(nome.strip()) == 0 or len(sexo.strip()) == 0 or len(idade.strip()) == 0 or len(email.strip()) == 0 or len(telefone.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos não podem está em branco.')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida.')
            return redirect('/pacientes/')

        paciente = Pacientes.objects.filter(email=email)

        if paciente.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente cadastrado com esse email.')
            return redirect('/pacientes/')

        try:
            pacientes = Pacientes(nome = nome,
                                  sexo = sexo,
                                  idade= idade,
                                  email = email,
                                  telefone = telefone,
                                  nutri = request.user)
            pacientes.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso.')
            return redirect('/pacientes/')
        except:
            messages.add_message(redirect, constants.ERROR, 'Erro interno do sistema.')
            return redirect('/pacientes/')


@login_required(login_url = "/auth/login/")
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes':pacientes})


@login_required(login_url='/auth/login/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(pacientes=paciente)
        return render(request, 'dados_pacientes.html', {'paciente':paciente,'dados_paciente':dados_paciente})
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        if len(peso.strip()) == 0 or len(altura.strip()) == 0 or len(gordura.strip()) == 0 or len(musculo.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos não podem ficar em branco')
            return redirect('/dados_paciente/')
        
        if len(hdl.strip()) == 0 or len(ldl.strip()) == 0 or len(colesterol_total.strip()) == 0 or len(triglicerídios.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos não podem ficar em branco')
            return redirect('/dados_paciente/')

        try:
            p1 = DadosPaciente(pacientes = paciente,
                                        peso = peso,
                                        altura = altura,
                                        percentual_gordura = gordura,
                                        percentual_musculo = musculo,
                                        colesterol_hdl = hdl,
                                        colesterol_ldl = ldl,
                                        colesterol_total = colesterol_total,
                                        trigliceridios = triglicerídios)
            p1.save()
            messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
            return redirect('/dados_paciente/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/dados_paciente/')


