from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required


from .forms import ItemForm
from .models import Items, Photos, Categories, Location


@login_required
def item_create_view(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ItemForm()

    context = {"form": form}

    return render(request, "itemmgmt/item_create.html", context)


@login_required
def item_detail_view(request):
    # obj = Items.objects.filter()
    obj = Items.objects.all()

    context = {"object": obj}

    return render(request, "itemmgmt/item_detail.html", context)


@login_required
def dynamic_lookup_view(request, my_id):
    try:
        obj = Items.objects.get(id=my_id)
    except Items.DoesNotExist:
        raise Http404

    context = {"object": obj}

    return render(request, "itemmgmt/dynamic_item_detail.html", context)
