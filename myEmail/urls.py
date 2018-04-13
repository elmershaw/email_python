"""myEmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from  emailClient.views  import *   #home,login,DisplyAllEmail

from django.contrib.auth.views import  logout

urlpatterns = [
    url(r'^$', login, name="login"),
    url(r'^home/$', home, name="home"),
    url(r'^inbox/$', inbox, name="inbox"),
    url(r'^outbox/$', outbox, name="outbox"),
    url(r'^send/$', send, name="send"),
    url(r'^contact/$', contact, name="contact"),
    url(r'^fecthall/$', fecthall, name="recvall"),
    url(r'^callsend/$', callsend, name="callsend"),
    url(r'^logout/$', logout, name="logout"),

    url(r'^admin/', admin.site.urls),
]


'''
  url(r'^index', 'emailClient.views.index', name='index'),
    url(r'^write', 'emailClient.views.write', name='write'),
    url(r'^inbox', 'emailClient.views.recvmail', name='recvmail'),
    url(r'^sendmail/$', 'emailClient.views.send_email', name='send_email'),
    url(r'^mainemail/$', 'emailClient.views.login', name='login'),
    url(r'^details', 'emailClient.views.reademail', name='reademail'),


'''
