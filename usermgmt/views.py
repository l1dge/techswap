from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login


# def index(request):
# return HttpResponse("Hello, world. You're at the usermgmt index.")
def index(request):
    return render(request, "usermgmt/index.html", {})


def tslogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        return render(request, "usermgmt/login_success.html", {})
    else:
        return render(request, "usermgmt/login_error.html", {})
