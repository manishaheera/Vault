
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'registration_login.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            user = User.objects.create(
                username = request.POST['username'],
                email = request.POST['email'],
                password = password_hash,
            )
            request.session['user_signed_in'] = user.id
            return redirect('/user/dashboard')

def user_dashboard(request):
    user = User.objects.get(id=request.session['user_signed_in'])
    context = {
        'user': User.objects.get(id=request.session['user_signed_in']),
    }
    return render(request,'dashboard.html', context)

def user_login(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            this_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_signed_in'] = this_user.id
                return redirect('/user/dashboard')    
        messages.error(request,"Vault account not found. Please try again.")
        return redirect('/')

def user_logout(request):
    request.session.flush()
    return redirect('/')