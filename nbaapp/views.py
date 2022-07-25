import json

from django.db import connection
from django.utils.datetime_safe import time
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from django.db.models import Count, Sum
from .form import LoginForm
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
import time
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
# 注册
from .models import *


def register(request):
    return render(request, "Outdated/register.html")



# 首页
def nba(request):
    return render(request, "nbaFirst.html")


def first(request):
    return render(request, "First.html")


def usercenter(request):
    return render(request, "blocks.html")


db = NbaappPlayer.objects.all()
db1 = db[:100]
db2 = db[100:200]
db3 = db[200:300]
db4 = db[300:]


teamdb = NbaappTeam.objects.all().order_by('team_range')
playerrange = db.order_by('-points')[:20]


# 第二页
def nbaSecond(request):
    return render(request, "nbaSecond.html", {"db": db1})


def nbaSecondse(request):
    playername = request.GET.get("playername")
    player = NbaappPlayer.objects.filter(name__icontains=playername)
    return render(request, "NbaSecondsearch.html", {"player": player})


def nbaSecond2(request):
    return render(request, "nbaSecond2.html", {"db": db2})


def nbaSecond3(request):
    return render(request, "nbaSecond3.html", {"db": db3})


def nbaSecond4(request):
    return render(request, "nbaSecond4.html", {"db": db4})


# 第三页
def nbaThird(request):
    return render(request, "NbaThird.html", {"db": playerrange})


# 第四页
def nbaForth(request):
    # print(teamdb[0]['img_url'])
    return render(request, "nbaForth.html", {"db": teamdb})

    # 注册时处理提交的数据


# 以下是注册
def Register(request):
    message = ""
    if request.method == "POST":
        global username
        username = request.POST.get("username")
        password = request.POST.get("password")
        comfirmpassword = request.POST.get("comfirmpassword")
        if username and password and comfirmpassword:
            username = username.strip()
            if AuthUser.objects.filter(username=username):
                message = "用户名已存在!"
                return render(request, "LogNew.html", {"message": message})
            if password != comfirmpassword:
                message = "确认密码必须和密码相同!"
                return render(request, "LogNew.html",{"message":message})
        # shift+F11快捷打开书签            # 需要加一个用户名已存在的判断
        dj_ps = make_password(password)
        user = User.objects.create(username=username, password=dj_ps
                                   , is_superuser=0, )

        user.save()
        request.session['username'] = username
    return render(request, "nbaFirst.html")



# 新版登录,增加了一些逻辑判断
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = AuthUser.objects.get(username=username)

                if check_password(password,user.password):
                    request.session['username'] = username
                    return render(request, 'nbaFirst.html')

                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'LogNew.html', {"message": message})

    return render(request, 'LogNew.html')

#登出
def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return render(request, 'LogNew.html')



def index_possession(request):
    username = request.session['username']
    obj = AuthUser.objects.get(username=username)
    try:
        team_amount = dict(NbaappTeam.objects.values_list('boss_name').annotate(amount=Count('*')))[username]
    except:
        team_amount = 0
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT * from nbaapp_teamboss  join nbaapp_team where nbaapp_teamboss.team_name = nbaapp_team.team_name;")
    #     row = cursor.fetchall()
    info = NbaappTeam.objects.raw(
        "SELECT * from nbaapp_team where boss_name = '%s'"
        % (username)
    )
    info2 = NbaappTeam.objects.raw(
        "SELECT * from nbaapp_team where boss_name != '%s'"
        % (username)
    )
    team_market = NbaappTeam.objects.all()

    return render(request, "index_possession.html",
                  {"db": obj, "team_amount": team_amount, "row": info, "team_market": team_market, "row2": info2, }, )


def index_possessionse(request):
    team_name = request.GET.get("team_name")
    team = NbaappTeam.objects.filter(team_name__icontains=team_name)
    return render(request, "index_possessionse.html", {"team": team})


def purchase(request):
    team_name = request.path.split('/')[2]
    username = request.session['username']
    print(request.session['username'])
    team = NbaappTeam.objects.get(team_name__exact=team_name)
    user = AuthUser.objects.get(username=username)
    return render(request, "forms.html", {'team': team, 'user': user})


def purchase_deal(request):
    # print(request)
    team_name = request.path.split('/')[2]
    team = NbaappTeam.objects.get(team_name__exact=team_name)
    username = request.session['username']
    trade_time = time.asctime(time.localtime(time.time()))
    value = team.value
    # print(value)
    # print(type(trade_time))
    if request.method == "POST":
        password = request.POST.get('password', None)
        if password:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            user = AuthUser.objects.get(username=username)
            if user.password == password:
                # return render(request, 'index_possessionse.html')
                NbaappTeam.objects.filter(team_name=team_name).update(trade_time=trade_time)
                NbaappTeam.objects.filter(team_name=team_name).update(boss_name=username)
                AuthUser.objects.raw(
                    "UPDATE auth_user SET reposite = (reposite-%f) where username = '%s'" % (value, username))

                # "UPDATE nbaapp_team set trade_time = '%s' where team_name = '%s'" % (trade_time, team_name))
                return redirect('/possession/')
            else:
                message = "密码不正确！"
        return render(request, 'forms.html', {"message": message, 'team': team, 'user': user})

def to_firstpage(request):
    return render(request,"NbaSecond.html")