from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def usuario_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='Admin').exists()
    )


def usuario_funcionario(user):
    return user.is_authenticated and user.groups.filter(name='Funcionario').exists()


def apenas_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if usuario_admin(request.user):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("Acesso negado. Apenas administradores podem executar esta ação.")

    return wrapper