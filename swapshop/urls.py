from django.urls import path

# from django.views.generic import TemplateView

from .views import (
    HomeView,
    AboutView,
    ContactView,
    SocialView,
    AllItemsView,
    ItemDetailView,
    GuestItemDetailView,
    ItemCreateView,
    AddToWishListView,
    MyWishListView,
    MySwapListView,
    ManageWishListView,
    EmptyWishListView,
    UserProfileView,
    UserItemDetailView,
    SearchView,
    SwapCreateView,
)

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
    path("additem/", ItemCreateView.as_view(), name="itemcreate"),
    path("additem/", SwapCreateView.as_view(), name="swapcreate"),
    path("add-to-list-<int:itm_id>/", AddToWishListView.as_view(), name="addtolist"),
    path("my-swap-list/", MySwapListView.as_view(), name="myswaplist"),
    path("my-wish-list/", MyWishListView.as_view(), name="mywishlist"),
    path("manage-list/<int:cp_id>/", ManageWishListView.as_view(), name="managelist"),
    path("empty-list/", EmptyWishListView.as_view(), name="emptylist"),
    path("accounts/profile/", UserProfileView.as_view(), name="userprofile"),
    path(
        "accounts/profile/item-<int:pk>/",
        UserItemDetailView.as_view(),
        name="useritemdetail",
    ),
    path("search/", SearchView.as_view(), name="search"),
]
