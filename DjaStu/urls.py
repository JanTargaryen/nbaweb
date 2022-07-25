"""DjaStu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# 路由文件
# 把指定功能模块的views导进来
from django.views.static import serve

from nbaapp import views
from django.conf.urls import url
from nbaapp import models

urlpatterns = [
    url(r'First', views.nba, name='nbaFirst'),
    url(r'usercenter', views.usercenter, name='usercenter'),
    url(r'^$', views.first, name='First'),
    url(r"^second/", include("nbaapp.urls")),
    url(r"third/", views.nbaThird, name='third'),
    url(r"forth/", views.nbaForth, name='forth'),
    url("deal/", views.Register),
    url(r'^admin/', admin.site.urls, name='admin'),
    url("register/", views.register, name='register'),
    url("login/", views.login, name='login'),
    url("secondse/", views.nbaSecondse, name='secondse'),
    url("possession/", views.index_possession, name='possession'),
    url('logout/', views.logout, name='logout'),
    url("index_possessionse/", views.index_possessionse, name="index_possessionse"),
    url("purchase/[\u4e00-\u9fa5]+/", views.purchase, name="purchase"),
    url("purchase_deal11/", views.purchase_deal, name="purchase_deal11"),

    # path('echart/<str:name>/', views.echart)
]

# 之前一直出不来:index前面多了个斜杠
