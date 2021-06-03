from django.urls import path

from swaplist.views import index

app_name = "swaplist"
urlpatterns = [
    path("", index, name="swap"),
]
