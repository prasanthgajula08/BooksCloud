from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from mainapp import models
import boto3
import datetime

# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST['uname']

        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if not username.isalnum():
            messages.info(request,'*username must be A-Z a-z 0-9')
            return render(request,'signup.html')
        elif len(password)<5:
            messages.info(request,'*password too short ')
            return render(request,'signup.html')
        elif password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'*username already exists')
                return render(request,'signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'*email already exists')
                return render(request,'signup.html')
            else:
                s=email
                s=s.replace('.','d')
                s=s.replace('@','a')
                u=username.replace(' ','s')
                bucket_name=u+'kumar'+s
                print(bucket_name)
                bucket_name=bucket_name.lower()
                client=boto3.client('s3')
                response = client.create_bucket(ACL='private',Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
                print('**************')
                print(response)
                user=User.objects.create_user(username=username,password=password,email=email)
                user.save()
                return render(request,'index.html')
        else:
            messages.info(request,'*password not matching')
            return render(request,'signup.html')
    else:
        return render(request,'signup.html')


def login(request):
    if request.method=="POST":
        username=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            data=models.File.objects.filter(username=request.user.username)
            return render(request,'home.html',{'data':data,'name':request.user.username})
        else:
            messages.info(request,'*invalid credentails')
            return render(request,'index.html')
    else:
        return render(request,'index.html')


def forgot(request):

    if request.method=="POST":
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
           OTP=get_random_string(length=6, allowed_chars='1234567890')
           html_content=OTP


           send_mail('Send mail',html_content, settings.EMAIL_HOST_USER,[email],fail_silently=False)

           return render(request,'otp.html')

        else:
            return render(request,'email.html')
    else:
        return render(request,'email.html')

def logout(request):
    auth.logout(request)
    return render(request,'home.html')
l=[]

def email(request):
    email=request.POST['email']
    if User.objects.filter(email=email).exists():
       username=User.objects.get(email=email)
       username=username.username
       OTP=get_random_string(length=6, allowed_chars='1234567890')
       html_content=OTP
       l.clear()
       l.append(str(OTP))
       print("****************************")
       print(l)
       send_mail('Send mail',html_content, settings.EMAIL_HOST_USER,[email],fail_silently=False)
       return render(request,'otp.html',{'uname':username,'email':email})
    else:
       messages.info(request,'*invalid email')
       l.clear()
       return render(request,'email.html')

def otp(request):
    otp=str(request.POST['otp'])
    temp=str(l[0])
    if temp==otp:
        uname=request.POST['username']
        email=request.POST['email']

        return render(request,'reset.html',{'uname':uname,'email':email})
    else:
        messages.info(request,'*invalid OTP')
        return render(request,'otp.html')
def check(request):
    username=request.POST['uname']
    email=request.POST['email']
    password=request.POST['password']
    password1=request.POST['password1']
    u=User.objects.get(username__exact=username)

    e=u.email
    print(e)
    print(email)
    print(username)
    print(u)
    print('***********++++++++++++')
    uname=username
    if password==password1:
        print("{}{}{}")
        if len(password)<5:
            messages.info(request,'*password too short ')
            return render(request,'reset.html',{'uname':uname,'email':email})
        elif str(username) == str(u) and str(email) == str(e):
            print('*********************')
            print(u.password)
            print(password)
            u.set_password(password)
            u.save()
            return render(request,'index.html')
        else:
             messages.info(request,'*invalid email or username')
             return render(request,'reset.html',{'uname':uname,'email':email})
    else:
         messages.info(request,'*password not matching')
         return render(request,'reset.html',{'uname':uname,'email':email})
