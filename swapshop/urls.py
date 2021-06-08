from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = "swapshop"
urlpatterns = [
    path("", ItemHomeView.as_view(), name="itemhome"),
    path("list/", ItemListView.as_view(), name="itemlist"),
    path(
        "create/",
        ItemCreateView.as_view(),
        name="itemcreate",
    ),
    path("itemdet/<int:pk>/", ItemDetailView.as_view(), name="itemdetail"),
    path("", index, name="swap"),
    path("register/", AppUserRegistrationView.as_view(), name="userregistration"),
    path("logout/", AppUserLogoutView.as_view(), name="userlogout"),
    path("login/", AppUserLoginView.as_view(), name="userlogin"),
    path("profile/", AppUserProfileView.as_view(), name="userprofile"),
    path(
        "profile/order-<int:pk>/",
        AppUserItemDetailView.as_view(),
        name="userorderdetail",
    ),
    path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
    path(
        "password-reset/<email>/<token>/",
        PasswordResetView.as_view(),
        name="passwordreset",
    ),
]
