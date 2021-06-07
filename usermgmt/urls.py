from django.urls import path

from .views import *

app_name = "usermgmt"
urlpatterns = [
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path(
        "profile/order-<int:pk>/",
        CustomerOrderDetailView.as_view(),
        name="customerorderdetail",
    ),
]
