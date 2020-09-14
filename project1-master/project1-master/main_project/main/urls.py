"""main URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from mainapp import views
from registrationsapp import views as v
from registrationsapp import urls as u
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login',v.login),
    path('delete',views.delete),
    path('upload',views.upload),
    path('accounts/',include(u)),
    path('remove',views.remove),
    path('search',views.search),
    path('share',views.share),
    path('sharefinal',views.sharefinal),
    path('sharedfiles',views.sharedfiles),
    path('shareddownload',views.shareddownload),
    path('receivedsearch',views.receivedsearch),
    path('profile',views.profile),
    path('mybooks',views.mybooks),
    path('chief',views.chief),
    path('profilereset',views.profilereset),
    path('shareddata',views.shareddata),
    path('stopreceiving',views.stopreceiving),
    path('removereceiving',views.removereceiving),
    path('profileresetpassword',views.profileresetpassword),
    path('changenewpassword',views.changenewpassword),
    path('thisis',views.thisis),
    path('sharedsearch',views.sharedsearch)
]
