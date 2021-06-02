from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_visits": num_visits,
    }
    return render(request, "home.html", context=context)


def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is all about TechSwap",
        "my_list": [123, 1234, 12345, 123456, 1234567],
    }
    return render(request, "about.html", my_context)


def social_view(request, *args, **kwargs):
    return render(request, "social.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})
