"""Ecommercesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('link/<name>/<user>/<email>',views.product_details,name='product_details'),
    path('cartitems/<email>/<name>/<path:image>',views.cartitems,name='cartitems'),
    path('payment',views.fullcarddetails,name='fullcarddetails'),
    path('gateway/<email>/<name>/<path:image>',views.gateway,name='gateway'),
    path('carddetails',views.Scarddetails,name='Scarddetails'),
    path('otp/',views.paymentForm,name='paymentForm'),
    path('verifypin/',views.verifypin,name='verifypin'),
    path('authpin',views.autheotp,name='authotp'),
    path('sucess/',views.success,name='success')
]
