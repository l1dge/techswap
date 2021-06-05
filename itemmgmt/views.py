from django.http import Http404
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, DetailView
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


class ItemHomeView(LoginRequiredMixin, TemplateView):
    template_name = "itemmgmt/itemhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_items = Item.objects.all().order_by("-id")
        paginator = Paginator(all_items, 8)
        page_number = self.request.GET.get("page")
        print(page_number)
        item_list = paginator.get_page(page_number)
        context["item_list"] = item_list
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "itemmgmt/itemcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("itemmgmt:itemcreate")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)


class ItemListView(LoginRequiredMixin, ListView):
    template_name = "itemmgmt/itemlist.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allitems"


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "itemmgmt/dynamicitemdetail.html"
    model = Item
    context_object_name = "item_obj"
