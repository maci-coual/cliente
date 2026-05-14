from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm, UserForm
from .models import Cliente

# Create your views here.

@login_required
def novo_cliente(request):
    clientes = Cliente.objects.all()
    template_name = 'novo_cliente.html'
    context = {}
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse('<h1>Deu erro no formulário</h1>')
    
    form = ClienteForm()
    context['form'] = form
    context['clientes'] = clientes

    return render(request, template_name, context)

@login_required
def atualizar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return HttpResponse('<h1>Cliente não encontrado</h1>')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('novo_cliente')
        else:
            return HttpResponse('<h1>Deu erro no formulário</h1>')
        
    form = ClienteForm(instance=cliente)
    template_name = 'novo_cliente.html'
    clientes = Cliente.objects.all()
    context = {
        'form': form,
        'clientes': clientes,
    }
    return render(request, template_name, context)

@login_required
def delete(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return HttpResponse('<h1>Cliente não encontrado</h1>')
    
    cliente.delete()
    return redirect('novo_cliente')


def login_usuario(request):
    template_name = 'login.html'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('novo_cliente')
        else:
            return HttpResponse('<h1>Usuário ou senha inválidos</h1>')
    else:
        form = AuthenticationForm()

    context = {'form': form}
        
    return render(request, template_name, context)


def novo_user(request):
    template_name = 'novo_user.html'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            return redirect('login_usuario')
        else:
            return HttpResponse('<h1>Deu erro no formulário</h1>')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def sair(request):
    logout(request)
    return redirect('login_usuario')