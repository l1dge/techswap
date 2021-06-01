from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponse

# from .forms import ItemForm
# from .models import Items, Photos, Categories, Location


def index(request):
    return render(request, "swaplist/index.html", {})
