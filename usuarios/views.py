from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario

def ativar_conta(request, token):
    usuario = get_object_or_404(Usuario, token_ativacao=token)

    if request.method == "POST":
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if senha != confirmar_senha:
            messages.error(request, "As senhas não conferem!")
        else:
            # cria usuário Django vinculado
            user = User.objects.create(
                username=usuario.email,
                email=usuario.email,
                password=make_password(senha),
                first_name=usuario.nome,
                is_active=True
            )

            # vincula ao cadastro e remove o token
            usuario.user = user
            usuario.token_ativacao = None
            usuario.save()

            messages.success(request, "Conta ativada com sucesso!")
            return redirect("login")  # redireciona para tela de login

    return render(request, "usuarios/ativar_conta.html", {"usuario": usuario})
