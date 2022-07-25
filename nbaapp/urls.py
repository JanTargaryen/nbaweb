from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

#路由文件
#把指定功能模块的views导进来
from nbaapp import views
from django.conf.urls import url
from nbaapp import models
urlpatterns = [
    url(r'^$',views.nbaSecond,name='second'),
    url(r'2/',views.nbaSecond2,name='second2'),
    url(r'3/',views.nbaSecond3,name='second3'),
    url(r'4/',views.nbaSecond4,name='second4'),

]
