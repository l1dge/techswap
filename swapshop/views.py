from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
)
from django.utils.text import slugify
from django.utils.timezone import now


from .forms import *
from .models import WishList, Item, User, WishListItem, User, Swap
from .utils import password_reset_token
from django.conf import settings
import logging


class SwapMixin(object):
    def dispatch(self, request, *args, **kwargs):
        list_id = request.session.get("list_id")
        if list_id:
            list_obj = WishList.objects.get(id=list_id)
            if request.user.is_authenticated and request.user.id:
                uid = User.objects.filter(pk=request.user.id).first()
                list_obj.client = uid
                list_obj.save()
        return super().dispatch(request, *args, **kwargs)

    def __str__(self):
        return f"WishList: {self.id}"


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["myname"] = "l1dge"
        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits
        all_items = Item.objects.all().order_by("-id")
        paginator = Paginator(all_items, 8)
        page_number = self.request.GET.get("page")
        item_list = paginator.get_page(page_number)
        context["item_list"] = item_list
        context["latest_items"] = all_items
        context["allcategories"] = Category.objects.all().order_by("title")
        return context


class AddToWishListView(LoginRequiredMixin, SwapMixin, TemplateView):
    template_name = "addtowishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        myitem_id = self.kwargs["itm_id"]
        item_obj = Item.objects.get(id=myitem_id)
        context["item_obj"] = item_obj

        # check if list exists
        list_id = self.request.session.get("list_id", None)
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
            list_obj = WishList.objects.get(id=list_id)
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


class ManageWishListView(LoginRequiredMixin, SwapMixin, View):
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


class EmptyWishListView(LoginRequiredMixin, SwapMixin, View):
    def get(self, request, *args, **kwargs):
        list_id = request.session.get("list_id", None)
        if list_id:
            item_list = WishList.objects.get(id=list_id)
            item_list.listitem_set.all().delete()
            item_list.save()
        return redirect("swapshop:mylist")


class MyWishListView(LoginRequiredMixin, SwapMixin, TemplateView):
    template_name = "useritemlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_id = self.request.session.get("list_id", None)
        if list_id:
            item_list = WishList.objects.get(id=list_id)
            items = WishListItem.objects.filter(item_list_id=item_list)
        else:
            item_list = None
        context["item_list"] = item_list
        context["items"] = items
        return context


class MySwapListView(LoginRequiredMixin, SwapMixin, TemplateView):
    template_name = "userswaplist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if user_id:
            items = Item.objects.filter(created_by=user_id)

        context["items"] = items
        return context


class UserRegistrationView(CreateView):
    template_name = "userregistration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("swapshop:userlogin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(
            username, password, email, first_name=first_name, last_name=last_name
        )
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("swapshop:home")


class UserLoginView(FormView):
    template_name = "userlogin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("swapshop:userprofile")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and User.objects.filter(username=uname).exists():
            login(
                self.request,
                usr,
                backend="allauth.account.auth_backends.AuthenticationBackend",
            )
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Invalid credentials"},
            )

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


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
        if not (Swap.objects.filter(wish_list__client=User).order_by("-id").exists()):
            items = None
        else:
            items = Swap.objects.filter(wish_list__client=User).order_by("-id")
        context["items"] = items
        return context


class AboutView(SwapMixin, TemplateView):
    template_name = "about.html"


class ContactView(SwapMixin, TemplateView):
    template_name = "contactus.html"


class SocialView(SwapMixin, TemplateView):
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


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/accounts/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META["HTTP_HOST"]
        # get User and then user
        User = User.objects.get(user__email=email)
        user = User.user
        # send mail to the user with email
        text_content = "Please Click the link below to reset your password. "
        html_content = (
            url
            + "/accounts/password-reset/"
            + email
            + "/"
            + password_reset_token.make_token(user)
            + "/"
        )
        send_mail(
            "Password Reset Link | TechSwap",
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/accounts/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("swapshop:passwordforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data["new_password"]
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)


# User Items List
class ItemCreateView(LoginRequiredMixin, SwapMixin, CreateView):
    template_name = "itemcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("swapshop:itemcreate")

    def form_valid(self, form):
        userid = self.request.user.id
        p = form.save(commit=False)
        p.created_by = self.request.user
        p.slug = (
            str(random.randint(50000, 600000)) + " " + str(p.created_by) + " " + p.title
        )
        p.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)


class ItemListView(LoginRequiredMixin, SwapMixin, ListView):
    template_name = "itemlist.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allitems"


class ItemDetailView(LoginRequiredMixin, SwapMixin, DetailView):
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


class GuestItemDetailView(SwapMixin, DetailView):
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


class AllItemsView(LoginRequiredMixin, SwapMixin, TemplateView):
    template_name = "allitems.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategories"] = Category.objects.all()
        return context


class SwapCreateView(LoginRequiredMixin, SwapMixin, CreateView):
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
