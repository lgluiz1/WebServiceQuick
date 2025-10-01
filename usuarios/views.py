from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Usuario

def ativar_conta(request, token):
    usuario = get_object_or_404(Usuario, token_ativacao=token)

    if request.method == "POST":
        senha = request.POST.get("senha")
        if senha:
            # cria usuário Django vinculado
            user = User.objects.create(
                username=usuario.email,
                email=usuario.email,
                password=make_password(senha),
                first_name=usuario.nome,
                is_active=True
            )
            # opcional: vincular user.id ao seu Usuario
            usuario.token_ativacao = None
            usuario.save()

            return redirect("login")  # redireciona para tela de login
    return render(request, "usuarios/ativar_conta.html", {"usuario": usuario})
