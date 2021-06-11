from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import *
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

from .forms import *
from .models import Cart, Item, AppUser, CartProduct, User, Swap
from .utils import password_reset_token
from django.conf import settings


class SwapMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.appuser:
                cart_obj.appuser = request.user.appuser
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(SwapMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["myname"] = "l1dge"
        # num_visits = request.session.get("num_visits", 0)
        # request.session["num_visits"] = num_visits + 1
        # context["num_visits"] = num_visits
        all_items = Item.objects.all().order_by("-id")
        paginator = Paginator(all_items, 8)
        page_number = self.request.GET.get("page")
        print(page_number)
        item_list = paginator.get_page(page_number)
        context["item_list"] = item_list
        return context


class AddToCartView(SwapMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs["itm_id"]
        item_obj = Item.objects.get(id=item_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_item_in_cart = cart_obj.cartitem_set.filter(item=item_obj)

            # item already exists in cart
            if this_item_in_cart.exists():
                cartitem = this_item_in_cart.last()
                cartitem.quantity += 1
                cart_obj.save()
            # new item is added in cart
            else:
                cartitem = CartProduct.objects.create(
                    cart=cart_obj,
                    item=item_obj,
                    quantity=1,
                )
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session["cart_id"] = cart_obj.id
            cartitem = CartProduct.objects.create(
                cart=cart_obj,
                item=item_obj,
                quantity=1,
            )
            cart_obj.save()

        return context


class ManageCartView(SwapMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("swapshop:mycart")


class EmptyCartView(SwapMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartitem_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("swapshop:mycart")


class MyCartView(SwapMixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context["cart"] = cart
        return context


class AppUserRegistrationView(CreateView):
    template_name = "userregistration.html"
    form_class = AppUserRegistrationForm
    success_url = reverse_lazy("swapshop:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AppUserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("swapshop:home")


class AppUserLoginView(FormView):
    template_name = "userlogin.html"
    form_class = AppUserLoginForm
    success_url = reverse_lazy("swapshop:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and AppUser.objects.filter(user=usr).exists():
            login(self.request, usr)
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


class AboutView(SwapMixin, TemplateView):
    template_name = "about.html"


class ContactView(SwapMixin, TemplateView):
    template_name = "contactus.html"


class SocialView(SwapMixin, TemplateView):
    template_name = "social.html"


class AppUserProfileView(TemplateView):
    template_name = "appuserprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and AppUser.objects.filter(user=request.user).exists()
        ):
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appuser = self.request.user.appuser
        context["appuser"] = appuser
        items = Swap.objects.filter(cart__client=appuser).order_by("-id")
        context["items"] = items
        return context


class AppUserItemDetailView(DetailView):
    template_name = "appuseritemdetail.html"
    model = Item
    context_object_name = "itm_obj"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and AppUser.objects.filter(user=request.user).exists()
        ):
            item_id = self.kwargs["pk"]
            item = Item.objects.get(id=item_id)
            if request.user.appuser != item.cart.appuser:
                return redirect("swapshop:userprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw)
        )
        print(results)
        context["results"] = results
        return context


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META["HTTP_HOST"]
        # get appuser and then user
        appuser = AppUser.objects.get(user__email=email)
        user = appuser.user
        # send mail to the user with email
        text_content = "Please Click the link below to reset your password. "
        html_content = (
            url
            + "/password-reset/"
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
    success_url = "/login/"

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


# Admin Pages


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = AppUserLoginForm
    success_url = reverse_lazy("swapshop:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Invalid credentials"},
            )
        return super().form_valid(form)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received"
        ).order_by("-id")
        return context


class AdminSwapDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminswapdetail.html"
    model = Swap
    context_object_name = "swp_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = SWAP_STATUS
        return context


class AdminSwapListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminswaplist.html"
    queryset = Swap.objects.all().order_by("-id")
    context_object_name = "allswaps"


class AdminSwapStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        swap_id = self.kwargs["pk"]
        swap_obj = Swap.objects.get(id=swap_id)
        new_status = request.POST.get("status")
        swap_obj.swap_status = new_status
        swap_obj.save()
        return redirect(
            reverse_lazy("swapshop:adminswapdetail", kwargs={"pk": swap_id})
        )


class AdminItemListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminitemlist.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allitems"


class AdminItemCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminitemcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("swapshop:adminitemlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)


# User Items List
class ItemCreateView(SwapMixin, CreateView):
    template_name = "itemcreate.html"
    form_class = ItemForm
    success_url = reverse_lazy("swapshop:itemcreate")

    def form_valid(self, form):
        userid = self.request.user.id
        p = form.save(commit=False)
        p.created_by = AppUser.objects.get(user_id=userid)
        p.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ItemImage.objects.create(item=p, image=i)
        return super().form_valid(form)


class ItemListView(SwapMixin, ListView):
    template_name = "itemlist.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allitems"


class ItemDetailView(SwapMixin, DetailView):
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


class AllItemsView(SwapMixin, TemplateView):
    template_name = "allitems.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategories"] = Category.objects.all()
        return context


# class ItemDetailView(SwapMixin, DetailView):
#     template_name = "itemdetail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         url_slug = self.kwargs["slug"]
#         item = Item.objects.get(slug=url_slug)
#         item.view_count += 1
#         item.save()
#         context["item"] = item
#         return context
