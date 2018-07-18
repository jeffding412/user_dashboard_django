from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt
from time import gmtime, strftime

def index(request):
    request.session.clear()
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

    request.session['user_id'] = user.id

    # redirect to a success route
    if  user.user_level == 9:
        return redirect('/dashboard/admin')

    return redirect('/dashboard')

def login_user(request):
    request.session['errors'] = User.objects.login_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        # return redirect('/blog/edit/'+id)
        return redirect('/signin')
    
    user = User.objects.filter(email=request.POST['email'])
    request.session['user_id'] = user[0].id
    if user[0].user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def logoff(request):
    request.session.clear()
    return redirect('/')

def admin(request):
    users = User.objects.all().values()
    for user in users:
        user['created_at'] = user['created_at'].strftime("%B. %d %Y")

    context = {
        "users": users
    }
    
    return render(request, "user_dashboard_app/admin.html", context)

def new_user(request):
    return render(request, "user_dashboard_app/new_user.html")

def create_new_user(request):
    request.session['errors'] = User.objects.basic_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        # return redirect('/blog/edit/'+id)
        return redirect('/users/new')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first'],last_name=request.POST['last'],email=request.POST['email'],password_hash=pw_hash,user_level=1,description="")

    return redirect('/dashboard/admin')

