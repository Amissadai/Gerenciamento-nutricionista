from asyncio import constants
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .utils import password_is_valid
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.WARNING, 'Usuário não cadastrado.')
            return redirect('/auth/login/')
        else:
            auth.login(request, usuario)
            return redirect('/')


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos não podem está vazio.')
            return redirect('/auth/cadastro/')
        
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro/')

        try:
            usuario = User.objects.create_user(username=username,
                                                email=email,
                                                password=senha,
                                                is_active=False)
            usuario.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect('/auth/login/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno de sistema.')
            return redirect('/auth/cadastro/')


        
        
