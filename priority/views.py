from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Clients_data
from .models import Clients


def index(request):
    return HttpResponse("Hello, world. I am in the priority part")

def client_submited(request):
    return render(request, 'client_submited.html')

@login_required(login_url='/users/login')
def clients_data(request):
    submitted = False
    if request.method == 'POST':
        form = Clients_data(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            return HttpResponseRedirect('/priority/client_submited')
    else:
        form = Clients_data()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'clients.html', {'form': form, 'submitted': submitted})

