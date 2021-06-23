from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = "swapshop"
urlpatterns = [
    # Client side pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("social/", SocialView.as_view(), name="social"),
    path("all-items/", AllItemsView.as_view(), name="allitems"),
    path("item/<slug:slug>/", ItemDetailView.as_view(), name="itemdetail"),
    path(
        "guestitem/<slug:slug>/", GuestItemDetailView.as_view(), name="guestitemdetail"
    ),
    path("add/", ItemCreateView.as_view(), name="itemcreate"),
    path("add-to-cart-<int:itm_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    # path(
    #     "accounts/register/",
    #     UserRegistrationView.as_view(),
    #     name="userregistration",
    # ),
    # path("accounts/logout/", UserLogoutView.as_view(), name="userlogout"),
    # path("accounts/login/", UserLoginView.as_view(), name="userlogin"),
    path("accounts/profile/", UserProfileView.as_view(), name="userprofile"),
    path(
        "accounts/profile/item-<int:pk>/",
        UserItemDetailView.as_view(),
        name="useritemdetail",
    ),
    path("search/", SearchView.as_view(), name="search"),
    # path(
    #     "accounts/forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"
    # ),
    # path(
    #     "accounts/password-reset/<email>/<token>/",
    #     PasswordResetView.as_view(),
    #     name="passwordreset",
    # ),
    # Admin Side pages
    # path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    # path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    # path(
    #     "admin-order/<int:pk>/", AdminSwapDetailView.as_view(), name="adminswapdetail"
    # ),
    # path("admin-all-orders/", AdminSwapListView.as_view(), name="adminswaplist"),
    # path(
    #     "admin-swap-<int:pk>-change/",
    #     AdminSwapStatusChangeView.as_view(),
    #     name="adminswapstatuschange",
    # ),
    # path("admin-item/list/", AdminItemListView.as_view(), name="adminitemlist"),
    # path(
    #     "admin-item/add/",
    #     AdminItemCreateView.as_view(),
    #     name="adminitemcreate",
    # ),
]
