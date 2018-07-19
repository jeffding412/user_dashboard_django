from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Post, Comment
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

def edit_information(request):
    request.session['errors'] = User.objects.edit_info_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/edit')

    current_user = User.objects.get(id = request.session['user_id'])
    current_user.first_name = request.POST['first']
    current_user.last_name = request.POST['last']
    current_user.email = request.POST['email']
    current_user.save()

    return redirect('/users/edit')

def edit_information(request, id):
    request.session['errors'] = User.objects.edit_info_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/edit/' + id)

    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    target_user.first_name = request.POST['first']
    target_user.last_name = request.POST['last']
    target_user.email = request.POST['email']
    if request.POST['level'] == 'Admin':
        target_user.user_level = 9
    else:
        target_user.user_level = 1

    target_user.save()

    return redirect('/users/edit/' + id)

def change_password(request):
    request.session['errors'] = User.objects.change_password_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/edit')

    current_user = User.objects.get(id = request.session['user_id'])
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    current_user.password_hash = pw_hash
    current_user.save()

    return redirect('/users/edit')

def change_password(request, id):
    request.session['errors'] = User.objects.change_password_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/edit/' + id)

    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    target_user.password_hash = pw_hash
    target_user.save()

    return redirect('/users/edit/' + id)

def edit_description(request):
    current_user = User.objects.get(id = request.session['user_id'])
    current_user.description = request.POST['description']
    current_user.save()

    return redirect('/users/edit')

def login_user(request):
    request.session['errors'] = User.objects.login_validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
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
    if not "user_id" in request.session:
        return redirect('/signin')
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

def delete_user(request, id):
    delete_id = int(id)
    target_user = User.objects.get(id = delete_id)
    target_user.delete()
    return redirect('/dashboard/admin')

def edit_profile(request):
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': current_user
    }
    return render(request, "user_dashboard_app/edit_profile.html", context)

def dashboard(request):
    if not "user_id" in request.session:
        return redirect('/signin')
    users = User.objects.all().values()
    for user in users:
        user['created_at'] = user['created_at'].strftime("%B. %d %Y")

    context = {
        "users": users
    }
    
    return render(request, "user_dashboard_app/dashboard.html", context)

def return_to_dashboard(request):
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def edit_user(request, id):
    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    context = {
        'user': target_user
    }
    return render(request, "user_dashboard_app/edit_user.html", context)

def show_info(request, id):
    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    target_user.created_at = target_user.created_at.strftime("%B %d %Y")
    context = {
        'user': target_user
    }
    return render(request, "user_dashboard_app/user.html", context)

def post(request, id):
    # to do
    return redirect('/users/show/' + id)