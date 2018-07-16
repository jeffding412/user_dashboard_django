from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    return render(request, "user_dashboard_app/index.html")

def sign_in(request):
    return render(request, "user_dashboard_app/signin.html")