from django.views.generic import (
    View,
    TemplateView,
    CreateView,
    FormView,
    DetailView,
    ListView,
)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from itemmgmt.models import *
import requests


# Create your views here.
def HomeView(request, *args, **kwargs):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_visits": num_visits,
    }
    return render(request, "home.html", context=context)


def AboutView(request, *args, **kwargs):
    my_context = {
        "my_text": "This is all about TechSwap",
        "my_list": [123, 1234, 12345, 123456, 1234567],
    }
    return render(request, "about.html", my_context)


def SocialView(request, *args, **kwargs):
    return render(request, "social.html", {})


def ContactView(request, *args, **kwargs):
    return render(request, "contact.html", {})


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(title__icontains=kw)
            | Q(description__icontains=kw)
            | Q(return_policy__icontains=kw)
        )
        print(results)
        context["results"] = results
        return context
