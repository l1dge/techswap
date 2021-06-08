from django.urls import path

from usermgmt.views import *

app_name = "usermgmt"
urlpatterns = [
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
