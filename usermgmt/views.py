from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# def index(request):
# return HttpResponse("Hello, world. You're at the usermgmt index.")
@login_required
def index(request):
    return render(request, "usermgmt/index.html", {})
