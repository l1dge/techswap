"""TechSwap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from pages.views import HomeView, AboutView, SocialView, ContactView, SearchView

urlpatterns = [
    path("usermgmt/", include("usermgmt.urls")),
    path("swaplist/", include("swaplist.urls")),
    path("itemmgmt/", include("itemmgmt.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomeView, name="home"),
    path("home/", HomeView, name="home"),
    path("about/", AboutView, name="about"),
    path("contact/", ContactView, name="contact"),
    path("social/", SocialView, name="social"),
    path("admin/", admin.site.urls),
    path("search/", SearchView.as_view(), name="search"),
]
