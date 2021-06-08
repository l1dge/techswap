from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
from itemmgmt.models import Item
import requests


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class AppUserHomeView(LoginRequiredMixin, TemplateView):
    template_name = "usermgmt/appuserhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_items = Item.objects.all().order_by("-id")
        paginator = Paginator(all_items, 8)
        page_number = self.request.GET.get("page")
        print(page_number)
        item_list = paginator.get_page(page_number)
        context["item_list"] = item_list
        return context


class AppUserRegistrationView(CreateView):
    template_name = "userregistration.html"
    form_class = AppUserRegistrationForm
    success_url = reverse_lazy("usermgmt:appuserhome")

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
        return redirect("usermgmt:appuserhome")


class AppUserLoginView(FormView):
    template_name = "userlogin.html"
    form_class = AppUserLoginForm
    success_url = reverse_lazy("usermgmt:appuserhome")

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


class AppUserProfileView(TemplateView):
    template_name = "userprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and User.objects.filter(user=request.user).exists()
        ):
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.user
        context["user"] = user
        orders = Item.objects.filter(cart__user=user).order_by("-id")
        context["orders"] = orders
        return context


class AppUserItemDetailView(DetailView):
    template_name = "useritemdetail.html"
    model = Item
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and User.objects.filter(user=request.user).exists()
        ):
            order_id = self.kwargs["pk"]
            order = Item.objects.get(id=order_id)
            if request.user.appuser != order.cart.appuser:
                return redirect("usermgmt:userprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


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
            return redirect(reverse("usermgmt:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data["new_password"]
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)
