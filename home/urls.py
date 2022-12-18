"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from home import views

admin.site.site_header = "all discount in one platform"
admin.site.index_title = "Welcome to all discount in one platform"
admin.site.site_title = " our website"
urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('signup', views.handleSignup, name="handelSignup"),
    path('search', views.search, name="search"),

    path("product_detail/<int:productId>", views.productDetail,name="product_detail"),
    path("search_product_detail/<int:productId>", views.searchProductDetail,name="search_product_detail")

]
