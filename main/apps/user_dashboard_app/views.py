from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "user_dashboard_app/index.html")

def signin(request):
    return render(request, "user_dashboard_app/signin.html")

def register(request):
    return render(request, "user_dashboard_app/register.html")

def register_user(request):

    request.session['errors'] = User.objects.basic_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        # return redirect('/blog/edit/'+id)
        return redirect('/register')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    level = 1
    if User.objects.count() == 0:
        level = 9
    user = User.objects.create(first_name=request.POST['first'],last_name=request.POST['last'],email=request.POST['email'],password_hash=pw_hash,user_level=level,description="")

    # redirect to a success route
    if level == 9:
        return redirect('/dashboard/admin')

    return redirect('/dashboard')

def login_user(request):
    # update later
    print(request.POST['email'])
    print(request.POST['password'])
    return redirect('/signin')

