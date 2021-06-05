from django.urls import path
from django.views.generic import TemplateView

from itemmgmt.views import (
    ItemListView,
    ItemCreateView,
    ItemHomeView,
    ItemDetailView,
)

app_name = "itemmgmt"
urlpatterns = [
    path("", ItemHomeView.as_view(), name="itemhome"),
    path("list/", ItemListView.as_view(), name="itemlist"),
    path(
        "create/",
        ItemCreateView.as_view(),
        name="itemcreate",
    ),
    path("itemdet/<int:pk>/", ItemDetailView.as_view(), name="itemdetail"),
]
