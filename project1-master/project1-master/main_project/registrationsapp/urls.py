from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('signup',views.signup),
    path('forgot',views.forgot),
    path('logout',views.logout),
    path('email',views.email),
    path('otp',views.otp),
    path('check',views.check)

]
