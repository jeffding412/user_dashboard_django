from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt
from time import gmtime, strftime

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
    if  user.user_level == 9:
        return redirect('/dashboard/admin')

    return redirect('/dashboard')

def login_user(request):
    user = User.objects.filter(email=request.POST['email'])
    if not user:
        request.session['failure'] = "No email/password combo" 
        return redirect('/signin')
    else:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password_hash.encode()):
            if user[0].user_level == 9:
                return redirect('/dashboard/admin')
            else:
                return redirect('/dashboard')
        else:
            request.session['failure'] = "No email/password combo" 
            return redirect('/signin')

def logoff(request):
    request.session.clear()
    return redirect('/')

def admin(request):
    users = User.objects.all().values()
    for user in users:
        user['created_at'] = user['created_at'].strftime("%B. %d %Y")
    
    return render(request, "user_dashboard_app/admin.html", {'users': users})