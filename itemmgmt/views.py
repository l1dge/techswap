from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
import requests


from .forms import ItemForm
from .models import Item, ItemImage


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "itemmgmt/item_create.html"
    form_class = ItemForm
    success_url = reverse_lazy("itemmgmt:itemcreate")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)


@login_required
def item_detail_view(request):
    # obj = Items.objects.filter()
    obj = Item.objects.all().order_by("-id")

    context = {"object": obj}

    return render(request, "itemmgmt/item_detail.html", context)


@login_required
def dynamic_lookup_view(request, my_id):
    try:
        obj = Item.objects.get(id=my_id)
    except Item.DoesNotExist:
        raise Http404

    context = {"item": obj}

    return render(request, "itemmgmt/dynamic_item_detail.html", context)
