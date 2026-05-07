from multiprocessing import context

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ClienteForm
from .models import Cliente

# Create your views here.

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

def delete(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return HttpResponse('<h1>Cliente não encontrado</h1>')
    
    cliente.delete()
    return redirect('novo_cliente')