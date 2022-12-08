from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, "backend/index.html")


def login(req):
    return render(req, "backend/login.html")


def register(req):
    return render(req, "backend/register.html")


def history(req):
    return render(req, "backend/history.html")
