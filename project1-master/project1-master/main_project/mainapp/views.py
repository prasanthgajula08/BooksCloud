from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from . import models
import sys
import boto3
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'home.html')
def upload(request):

    if request.method=="POST":
        print('*************')
        uploadfile=request.FILES['document']

        print('************************')
        log=request.user.username
        if len(log) ==0:
            messages.info(request,'*please login')
            return render(request,'index.html')
        else:
            bookname=request.POST['book']
            b=bookname+log

            if  models.File.objects.filter(filename=b).exists():
                messages.info(request,'*book name is already available in your repository')
                data=models.File.objects.filter(username=request.user.username)
                return render(request,'home.html',{'data':data})

            else:
                client=boto3.client('s3')
                email= User.objects.get(username=log)
                email=email.email
                s=email
                data=uploadfile.read()
                s=s.replace('.','d')
                s=s.replace('@','a')
                u=log.replace(' ','s')
                bucket_name=log+'kumar'+s
                bucket_name=bucket_name.lower()
                print(bucket_name)
                res=client.put_object(ACL='public-read',Body=data,Bucket=bucket_name,Key=bookname)
                print('************************')
                print('object has been uploaded')
                url="https://"+bucket_name+".s3.ap-south-1.amazonaws.com/"+bookname
                print(url)
                data=models.File(username=log,filename=bookname+log,filename_real=bookname,url=url)
                data.save()
                data=models.File.objects.filter(username=request.user.username)
                print(type(uploadfile))
                return render(request,'home.html',{'data':data})
    else:
        data=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data})


def delete(request):
    if request.method=="POST":
        log=request.user.username
        filename=request.POST['filename']
        s3_client = boto3.client('s3')
        email= User.objects.get(username=log)
        email=email.email
        s=email
        s=s.replace('.','d')
        s=s.replace('@','a')
        u=log.replace(' ','s')
        bucket_name=u+'kumar'+s
        bucket_name=bucket_name.lower()
        '''s3_client.download_file(bucket_name, filename, filename)'''
        url="https://"+bucket_name+".s3.ap-south-1.amazonaws.com/"+filename
        print(url)
        '''http://chrome1kumarchrome1agmaildcom.s3.ap-south-1.amazonaws.com/java
        https://chrome1kumarchrome1agmaildcom.s3.ap-south-1.amazonaws.com/java'''
        data=models.File.objects.filter(username=request.user.username)
        print('file has been downloaded')
        return render(request,'home.html',{'data':data})
    else:
        data=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data})


def remove(request):
    print('***********remove**********')
    if request.method=="POST":
        filename_real=request.POST['filename1']
        log=request.user.username
        filename=filename_real+log
        print(filename)

        data=models.Backup(username=log,filename=filename,filename_real=filename_real,url='')
        data.save()
        data=models.File.objects.get(filename=filename).delete()
        data=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data})
    else:
        data=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data})

def search(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        print(pattern)
        print(log)
        data= models.File.objects.filter(Q(filename_real=pattern) & Q(username=request.user.username))

        if len(data):
            return render(request,'home.html',{'data':data})
        else:
            book='Book '+pattern+' not found'
            messages.info(request,book)
            return render(request,'home.html',{'data':data})
    else:
        data=models.File.objects.filter(username=request.user.username)
        return render(request,'home.html',{'data':data})

def share(request):
    if request.method=="POST":
        sharefile=request.POST['sharefile']
        return render(request,'share.html',{'file':sharefile})

def sharefinal(request):
    if request.method=="POST":
        sharefile=request.POST['sharefile']
        username=request.POST['username']
        print(sharefile)
        print(username)
        if User.objects.filter(username=username).exists():
            log=request.user.username
            filename=sharefile
            email= User.objects.get(username=log)
            remail=User.objects.get(username=username)
            remail=remail.email
            email=email.email
            s=email
            s=s.replace('.','d')
            s=s.replace('@','a')
            u=log.replace(' ','s')
            bucket_name=u+'kumar'+s
            bucket_name=bucket_name.lower()
            sender_name=log
            receiver_name=username
            shared_filename=sharefile
            sender_email=email
            receiver_email=remail

            print(bucket_name)
            print(sender_name)
            print(receiver_name)
            print(shared_filename)
            print(sender_email)
            print(receiver_email)
            l=[sender_name,receiver_name,bucket_name,sender_email,receiver_email,shared_filename]
            print(l)
            url="https://"+bucket_name+".s3.ap-south-1.amazonaws.com/"+shared_filename
            print(url)
            store=models.SharedFiles(sender_name=sender_name,receiver_name=receiver_name,bucket_name=bucket_name,sender_email=sender_email,receiver_email=receiver_email,shared_filename=shared_filename,real_filename= url )
            store.save()
            #write message
            data=models.File.objects.filter(username=request.user.username)
            return render(request,'home.html',{'data':data})
        else:
            messages.info(request,'Given username is does not exists')
            return render(request,'share.html',{'file':sharefile})


def sharedfiles(request):
    username=request.user.username
    data=models.SharedFiles.objects.filter(receiver_name=username)
    return render(request,'sharedfiles.html',{'data':data})


def shareddownload(request):
    log=request.user.username
    if request.method=="POST":
        log=request.user.username
        bucket_name=request.POST['bucket_name']
        filename=request.POST['filename']
        data=models.SharedFiles.objects.filter(receiver_name=log)

        return render(request,'sharedfiles.html',{'data':data})
    else:
        data=models.SharedFiles.objects.filter(receiver_name=log)
        return render(request,'sharedfiles.html',{'data':data})

def receivedsearch(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        data= models.SharedFiles.objects.filter(Q(shared_filename=pattern) & Q(receiver_name=request.user.username))
        if len(data):
            return render(request,'sharedfiles.html',{'data':data})
        else:
            books='Book '+pattern+" not found"
            messages.info(request,books)
            return render(request,'sharedfiles.html',{'data':data})

    else:
        data=models.SharedFiles.objects.filter(receiver_name=log)
        return render(request,'sharedfiles.html',{'data':data})


def profile(request):
    return render(request,'profile.html')

def mybooks(request):
    data=models.File.objects.filter(username=request.user.username)
    return render(request,'home.html',{'data':data})

def chief(request):
    username=request.user.username
    email=User.objects.get(username=username)
    email=email.email
    return render(request,'Chief.html',{'username':username,'email':email})

def profilereset(request):
    print(request.POST['username'])
    print(request.POST['email'])
    return render(request,'Chief.html')

def shareddata(request):
    data=models.SharedFiles.objects.filter(sender_name=request.user.username)
    return render(request,'shareddata.html',{'data':data})

def stopreceiving(request):
    current_user=request.user.username
    receiver=request.POST['receiver']
    filename=request.POST['filename']
    data=models.SharedFiles.objects.filter(Q(sender_name=current_user) & Q(receiver_name=receiver) & Q(shared_filename=filename)).delete()
    data=models.SharedFiles.objects.filter(sender_name=request.user.username)
    return render(request,'shareddata.html',{'data':data})
def removereceiving(request):
     file=request.POST['filename1']
     user=request.user.username
     print(user,file)
     data=models.SharedFiles.objects.filter(Q(receiver_name=user) & Q(shared_filename=file)).delete()
     data=models.SharedFiles.objects.filter(receiver_name=user)
     return render(request,'sharedfiles.html',{'data':data})

def profileresetpassword(request):
    return render(request,'profileresetpassword.html')

def changenewpassword(request):
    pass1=request.POST['password']
    pass2=request.POST['password1']
    user=request.user.username
    if pass1==pass2:
        if len(pass1)<5:
            messages.info(request,'*password too short ')
            return render(request,'profileresetpassword.html')
        else:
            print('***************')
            u=User.objects.get(username=user)
            print("************")
            print(u)
            u.set_password(pass1)
            u.save()
            auth.logout(request)
            return render(request,'home.html')
    else:
        messages.info(request,'*password is not matching ')
        return render(request,'profileresetpassword.html')


def thisis(request):
    return render(request,'thisis.html')


def sharedsearch(request):
    if request.method=="POST":
        pattern=request.POST['search']
        log=request.user.username
        data= models.SharedFiles.objects.filter(Q(shared_filename=pattern) & Q(sender_name=request.user.username))
        if len(data):
            return render(request,'shareddata.html',{'data':data})
        else:
            books='Book '+pattern+" not found"
            messages.info(request,books)
            return render(request,'shareddata.html',{'data':data})
