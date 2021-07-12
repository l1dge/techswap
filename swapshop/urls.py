from django.urls import path

# from django.views.generic import TemplateView

from .views import (
    HomeView,
    AboutView,
    AllItemsView,
    ItemDetailView,
    GuestItemDetailView,
    ItemCreateView,
    AddToWishListView,
    MyWishListView,
    MyItemListView,
    ManageWishListView,
    EmptyWishListView,
    UserProfileView,
    UserItemDetailView,
    SearchView,
    RemWishListItemView,
    RemMyItemView,
    ArcMyItemView,
    NotYourItemView,
    MySwapListView,
    RequestSwapView,
    EmptySwapListView,
    RemSwapListItemView,
    SwapDetailView,
    AddToSwapListView,
    WLItemDetailView,
    AlreadyRequestedView,
    SuccessView,
    SwapSuccessView,
)

app_name = "swapshop"
urlpatterns = [
    # Client side pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView, name="about"),
    path("success/", SuccessView, name="success"),
    path("swapsuccess/", SwapSuccessView, name="swapsuccess"),
    path("all-items/", AllItemsView.as_view(), name="allitems"),
    path("item/<slug:slug>/", ItemDetailView.as_view(), name="itemdetail"),
    path("wlitem/<slug:slug>/", WLItemDetailView.as_view(), name="wlitemdetail"),
    path("swap/<slug:slug>/", SwapDetailView.as_view(), name="swapdetail"),
    path(
        "guestitem/<slug:slug>/", GuestItemDetailView.as_view(), name="guestitemdetail"
    ),
    path("additem/", ItemCreateView.as_view(), name="itemcreate"),
    path("add-to-wlist-<int:itm_id>/", AddToWishListView.as_view(), name="addtowlist"),
    path("add-to-slist-<int:itm_id>/", AddToSwapListView.as_view(), name="addtoslist"),
    path("my-item-list/", MyItemListView.as_view(), name="myitemlist"),
    path("my-wish-list/", MyWishListView.as_view(), name="mywishlist"),
    path("my-swap-list/", MySwapListView.as_view(), name="myswaplist"),
    path("manage-list/<int:cp_id>/", ManageWishListView.as_view(), name="managelist"),
    path("emptywishlist/", EmptyWishListView.as_view(), name="emptywishlist"),
    path("rem-wlitem/<slug:slug>/", RemWishListItemView.as_view(), name="remwlitem"),
    path("rem-myitem/<slug:slug>/", RemMyItemView.as_view(), name="remmyitem"),
    path("arc-myitem/<slug:slug>/", ArcMyItemView.as_view(), name="arcmyitem"),
    path("emptyswaplist/", EmptySwapListView.as_view(), name="emptyswaplist"),
    path("rem-slitem/<slug:slug>/", RemSwapListItemView.as_view(), name="remslitem"),
    path("reqswap-<int:itm_id>/", RequestSwapView, name="reqswap"),
    path("notyouritem/", NotYourItemView.as_view(), name="notyouritem"),
    path("alreadyrequested/", AlreadyRequestedView.as_view(), name="alreadyrequested"),
    path("accounts/profile/", UserProfileView.as_view(), name="userprofile"),
    path(
        "accounts/profile/item-<int:pk>/",
        UserItemDetailView.as_view(),
        name="useritemdetail",
    ),
    path("search/", SearchView.as_view(), name="search"),
]
