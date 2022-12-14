from django.shortcuts import render, redirect
from .models import Record

# Create your views here.

def index(req):
    return redirect('/auths')

def history(req):
    if(req.method == 'POST'):
        user = auth.username
        if (user):
            record = Record()
            record.date = date()
            record.user = user.name
            record.status = 'Approved'
            date.save()
        else:
            message.success(req, ('Invalid user'))
            return redirect('/history')
    else:
        records = Record.objects.filter(user=req.user)
        context = {'records': records}
        return render(req, "backend/history.html", context)


def include(req):
    return render(req, "backend/include.html")


def userList(req):
    return render(req, "backend/userList.html")


def user(req, id):
    return render(req, "backend/user.html")


def register(req):
    # if not req.user.is_authenticated:
    #     return render(req, "backend/error.html")
        
    return render(req, "backend/register.html")
