from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import UsuarioForm
from .models import Usuario


@require_GET
def home(request):
    return render(request, "usuarios/home.html", {"form": UsuarioForm()})


@require_http_methods(["GET", "POST"])
def usuarios(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            # Atualizar a página de destino repete apenas a consulta, sem outro cadastro.
            return redirect("listagem_usuarios")
        return render(request, "usuarios/home.html", {"form": form}, status=400)

    return render(request, "usuarios/usuarios.html", {
        "usuarios": Usuario.objects.order_by("id_usuario"),
    })
