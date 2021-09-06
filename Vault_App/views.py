
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            print(password_hash)
            user = User.objects.create(
            username = request.POST['username'],
            email = request.POST['email'],
            password = password_hash,
            )
            request.session['user_signed_in'] = user.id
            return redirect('/dashboard')

def dashboard(request):
    user = User.objects.get(id=request.session['user_signed_in'])
    context = {
        'user': User.objects.get(id=request.session['user_signed_in']),
    }
    return render(request,'dashboard.html', context)

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            this_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_signed_in'] = this_user.id
                return redirect('/dashboard')    
        messages.error(request,"ACCOUNT NOT FOUND, PLEASE VERIFY EMAIL/PASSWORD FIELDS ARE CORRECT")
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')