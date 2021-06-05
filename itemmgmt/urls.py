from django.urls import path
from django.views.generic import TemplateView

from itemmgmt.views import item_detail_view, ItemCreateView, dynamic_lookup_view

app_name = "itemmgmt"
urlpatterns = [
    path("", item_detail_view, name="item"),
    path(
        "create/",
        ItemCreateView.as_view(),
        name="itemcreate",
    ),
    path("itemdet/<int:my_id>/", dynamic_lookup_view, name="itemdet"),
]
