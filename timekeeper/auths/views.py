from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('/history')
        else:
            messages.success(req, ('There was an error loggin in, try again'))
            return redirect('/auths')

    else:
        return render(req, "authenticate/login.html", {})
