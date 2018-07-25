from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Post, Comment
import bcrypt
from time import gmtime, strftime
import hashlib
from datetime import datetime

def checkUserHash(user_id, user_hash):
    if hashlib.md5(str(user_id).encode()).hexdigest() != user_hash:
        return False
    else:
        return True

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

    request.session['user_id'] = user.id
    request.session['user_hash'] = hashlib.md5(str(request.session['user_id']).encode()).hexdigest()

    # redirect to a success route
    if  user.user_level == 9:
        return redirect('/dashboard/admin')

    return redirect('/dashboard')

def edit_my_information(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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

def change_my_password(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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
    request.session['user_hash'] = hashlib.md5(str(request.session['user_id']).encode()).hexdigest()

    if user[0].user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def logoff(request):
    request.session.clear()
    return redirect('/')

def admin(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    users = User.objects.all().values()
    for user in users:
        user['created_at'] = user['created_at'].strftime("%B. %d %Y")

    context = {
        "users": users
    }
    
    return render(request, "user_dashboard_app/admin.html", context)

def new_user(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    return render(request, "user_dashboard_app/new_user.html")

def create_new_user(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

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
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    delete_id = int(id)
    target_user = User.objects.get(id = delete_id)
    target_user.delete()
    return redirect('/dashboard/admin')

def edit_profile(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': current_user
    }
    return render(request, "user_dashboard_app/edit_profile.html", context)

def dashboard(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    users = User.objects.all().values()
    for user in users:
        user['created_at'] = user['created_at'].strftime("%B. %d %Y")

    context = {
        "users": users
    }
    
    return render(request, "user_dashboard_app/dashboard.html", context)

def return_to_dashboard(request):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def edit_user(request, id):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    context = {
        'user': target_user
    }
    return render(request, "user_dashboard_app/edit_user.html", context)

def show_info(request, id):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    target_id = int(id)
    target_user = User.objects.get(id = target_id)
    target_user.created_at = target_user.created_at.strftime("%B %d %Y")
    
    posts = Post.objects.filter(receiver=int(id))
    for post in posts:
        # s1 = str(post.created_at)
        # s2 = str(datetime.now())
        # FMT = '%H:%M:%S'
        # tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        # print(tdelta)
        # #strftime("%B. %d %Y"))
        # print(s1)
        # print(s2)
        comments = post.replies.all()
        for comment in comments:
            # still gotta figure out the time problem
            comment.display_time = comment.created_at.strftime("%B %d %Y")
            print(comment.display_time)
            comment.save()
        post.created_at = post.created_at.strftime("%B %d %Y")
    
    context = {
        'user': target_user,
        'posts': posts,
    }
    return render(request, "user_dashboard_app/user.html", context)

def post(request, id):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    target_user = User.objects.get(id = int(id))
    post_user = User.objects.get(id = request.session['user_id'])
    post = Post.objects.create(message=request.POST['message'], poster=post_user, receiver=target_user)
    return redirect('/users/show/' + id)

def comment(request, user_id, post_id):
    if not "user_id" in request.session:
        return redirect('/logoff')
    elif not checkUserHash(request.session['user_id'],request.session['user_hash']):
        return redirect('/logoff')

    commenter = User.objects.get(id = request.session['user_id'])
    post = Post.objects.get(id= int(post_id))
    comment = Comment.objects.create(message=request.POST['message'], commenter=commenter, post=post)
    return redirect('/users/show/' + user_id)