from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    View,
)

from .forms import UserRegistrationForm, UserProfileForm, UserAddressForm, ItemForm
from .models import (
    WishList,
    Item,
    User,
    WishListItem,
    User,
    Swap,
    Category,
    ItemImage,
    SwapList,
    SwapListItem,
)
from django.conf import settings
import random


class SwapWLMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            uid = User.objects.filter(pk=request.user.id).first()
            list_id = WishList.objects.get(client_id=uid)
            if list_id:
                list_obj = WishList.objects.get(client_id=uid)
                list_obj.client = uid
                list_obj.save()
            return super().dispatch(request, *args, **kwargs)

    def __str__(self):
        return f"WishList: {self.id}"


class SwapSLMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            uid = User.objects.filter(pk=request.user.id).first()
            list_id = SwapList.objects.get_or_create(client_id=uid.id)
            if list_id:
                list_obj = SwapList.objects.get(client_id=uid)
                list_obj.client = uid
                list_obj.save()
            return super().dispatch(request, *args, **kwargs)

    def __str__(self):
        return f"SwapList: {self.id}"


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["myname"] = "l1dge"
        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits
        all_items = Item.objects.all().order_by("-id")
        popular_items = all_items.order_by("view_count")
        paginator = Paginator(all_items, 8)
        page_number = self.request.GET.get("page")
        item_list = paginator.get_page(page_number)
        context["item_list"] = item_list
        context["latest_items"] = all_items
        context["popular_items"] = popular_items
        context["allcategories"] = Category.objects.all().order_by("title")
        return context


class AddToWishListView(LoginRequiredMixin, SwapWLMixin, TemplateView):
    template_name = "addtowishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        myitem_id = self.kwargs["itm_id"]
        item_obj = Item.objects.get(id=myitem_id)
        context["item_obj"] = item_obj

        # check if list exists
        user_id = self.request.user.id
        list_id = WishList.objects.filter(client_id=user_id).first()
        if not list_id:
            list_obj = WishList.objects.create()
            self.request.session["list_id"] = list_obj.id
            WishListItem.objects.create(
                item_list=list_obj,
                item=item_obj,
            )
            context["item_exists"] = False
            return context

        else:
            list_obj = WishList.objects.get(id=list_id.id)
            # item doesn't already exist in list
            list_item = list_obj.wishlistitem_set.filter(item_id=myitem_id)
            if list_item:

                context["item_exists"] = True
                return context
            else:
                WishListItem.objects.create(
                    item_list=list_obj,
                    item=item_obj,
                )

                context["item_exists"] = False
                return context


class ManageWishListView(LoginRequiredMixin, SwapWLMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = WishListItem.objects.get(id=cp_id)
        list_obj = cp_obj.list

        if action == "rmv":
            cp_obj.delete()
        else:
            pass
        return redirect("swapshop:mylist")


class EmptyWishListView(LoginRequiredMixin, SwapWLMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list_id = WishList.objects.filter(client_id=user_id).first()
        if list_id:
            item_list = WishList.objects.get(id=list_id.id)
            item_list.wishlistitem_set.all().delete()
            item_list.save()
        return redirect("swapshop:mywishlist")


class RemWishListItemView(LoginRequiredMixin, SwapWLMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list_id = WishList.objects.filter(client_id=user_id).first()
        if list_id:
            item_list = WishList.objects.get(id=list_id.id)
            url_slug = self.kwargs["slug"]
            item = Item.objects.get(slug=url_slug)
            item_list.wishlistitem_set.filter(item_id=item).delete()
            item_list.save()
        return redirect("swapshop:mywishlist")


class RemMyItemView(LoginRequiredMixin, SwapWLMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if user_id:
            url_slug = self.kwargs["slug"]
            item = Item.objects.filter(slug=url_slug)
            if user_id == item.created_by_id:
                item.delete()
                return redirect("swapshop:myitemlist")
            else:
                return redirect("swapshop:notyouritem")


class ArcMyItemView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if user_id:
            url_slug = self.kwargs["slug"]
            item = Item.objects.get(slug=url_slug)
            if user_id == item.created_by_id:
                item.archived = True
                item.save()
                return redirect("swapshop:myitemlist")
            else:
                return redirect("swapshop:notyouritem")


class MyWishListView(LoginRequiredMixin, SwapWLMixin, TemplateView):
    template_name = "useritemwishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        list_id = WishList.objects.filter(client_id=user_id).first()
        if list_id:
            item_list = WishList.objects.get(id=list_id.id)
            items = WishListItem.objects.filter(item_list_id=item_list)
        else:
            item_list = None
        context["item_list"] = item_list
        context["items"] = items
        return context


class MySwapListView(LoginRequiredMixin, SwapSLMixin, TemplateView):
    template_name = "useritemswaplist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        list_id = SwapList.objects.filter(client_id=user_id).first()
        if not list_id:
            list_obj = SwapList.objects.create()
            self.request.session["list_id"] = list_obj.id
            item_list = None
            context["item_list"] = item_list
            return context
        else:
            item_list = SwapList.objects.get(id=list_id.id)
            items = SwapListItem.objects.filter(item_list_id=item_list)
            context["item_list"] = item_list
            context["items"] = items
            return context


class MyItemListView(LoginRequiredMixin, SwapSLMixin, TemplateView):
    template_name = "useritemlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if user_id:
            items = Item.objects.filter(created_by=user_id)

        context["items"] = items
        return context


class UserProfileView(TemplateView):
    template_name = "userprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated
            and User.objects.filter(id=request.user.id).exists()
        ):
            return redirect("/accounts/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = self.request.user.id
        context["User"] = User
        swaps = Swap.objects.filter(wish_list__client=User).order_by("-id")
        items = swaps if swaps else None
        context["items"] = items
        return context


class NotYourItemView(SwapWLMixin, TemplateView):
    template_name = "notyours.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contactus.html"


class SocialView(TemplateView):
    template_name = "social.html"


class UserItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "useritemdetail.html"
    model = Item
    context_object_name = "itm_obj"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and User.objects.filter(user=request.user).exists()
        ):
            item_id = self.kwargs["pk"]
            item = Item.objects.get(id=item_id)
            if request.user.User != item.item_list.User:
                return redirect("swapshop:userprofile")
            else:
                return redirect("/accounts/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw)
        )
        context["results"] = results
        return context


# User Items List
class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "itemcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("swapshop:itemcreate")
    MINITEMID = 50000
    MAXITEMID = 600000
    RNDITMNO = str(random.randint(MINITEMID, MAXITEMID))

    def form_valid(self, form):
        # userid = self.request.user.id
        itm = form.save(commit=False)
        itm.created_by = self.request.user
        itm.slug = f"{self.RNDITMNO} {itm.created_by} {itm.title}"
        itm.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=itm, image=i)
        return super().form_valid(form)


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "dynamicitemdetail.html"
    queryset = Item.objects.all()
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs["slug"]
        item = Item.objects.get(slug=url_slug)
        item.view_count += 1
        item.save()
        context = {"item_obj": item, "API_KEY": settings.LOCATION_API_KEY}
        return context


class GuestItemDetailView(DetailView):
    template_name = "guestdynamicitemdetail.html"
    queryset = Item.objects.all()
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs["slug"]
        item = Item.objects.get(slug=url_slug)
        item.view_count += 1
        item.save()
        context = {"item_obj": item}
        return context


class AllItemsView(LoginRequiredMixin, TemplateView):
    template_name = "allitems.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategories"] = Category.objects.all()
        return context


class SwapCreateView(LoginRequiredMixin, CreateView):
    template_name = "swapcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("swapshop:myswaplist")

    def form_valid(self, form):
        userid = self.request.user.id
        p = form.save(commit=False)
        p.created_by = self.request.user
        p.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)
