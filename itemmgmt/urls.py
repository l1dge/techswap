from django.urls import path

# from . import views
from itemmgmt.views import item_detail_view, item_create_view, dynamic_lookup_view

app_name = "swaplist"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", item_detail_view, name="item"),
    path("create/", item_create_view, name="create"),
    path("itemdet/<int:my_id>/", dynamic_lookup_view, name="itemdet"),
]
