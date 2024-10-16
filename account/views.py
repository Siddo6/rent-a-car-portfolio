from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.
def user_login (request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            cd= form.cleaned_data
            user = authenticate (request,
                                 username=cd['username'],
                                 password=cd['password'])
            if user is not None:
                    login(request, user)
                    return redirect('index')  
            else:
                return HttpResponse('Your credentials are not correct')
            
    else:
            form= LoginForm()
            
    return render (request, 'account/login.html', {'form':form}) 

#logout view
def user_logout (request):
    logout(request)
    return redirect('index')