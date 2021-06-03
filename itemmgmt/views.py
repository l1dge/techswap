from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponse
from .forms import ItemForm
from .models import Items, Photos, Categories, Location


# def index(request):
#     return HttpResponse("Hello, world. You're at the itemmgmt index.")


def item_create_view(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ItemForm()

    context = {"form": form}

    return render(request, "itemmgmt/item_create.html", context)


# Create your views here.
def item_detail_view(request):
    # obj = Items.objects.get(id=1)
    obj = Items.objects.filter()

    # context = {
    #     "title": obj.title,
    #     "description": obj.description,
    #     "summary": obj.summary,
    # }
    context = {"object": obj}

    return render(request, "itemmgmt/item_detail.html", context)


def dynamic_lookup_view(request, my_id):
    # obj = get_object_or_404(Items, id=my_id)
    # obj = Items.objects.get(id=my_id)
    # obj = Items.objects.filter()
    try:
        obj = Items.objects.get(id=my_id)
    except Items.DoesNotExist:
        raise Http404

    # context = {
    #     "title": obj.title,
    #     "description": obj.description,
    #     "summary": obj.summary,
    # }
    context = {"object": obj}

    return render(request, "itemmgmt/dynamic_item_detail.html", context)
