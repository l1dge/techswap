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
    path("accounts/profile/", UserProfileView.as_view(), name="userprofile"),
    path(
        "accounts/profile/item-<int:pk>/",
        UserItemDetailView.as_view(),
        name="useritemdetail",
    ),
    path("search/", SearchView.as_view(), name="search"),
]
