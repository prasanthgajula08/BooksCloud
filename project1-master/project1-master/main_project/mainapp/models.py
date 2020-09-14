from django.db import models

# Create your models here.
class File(models.Model):
    username=models.CharField(max_length=90)
    filename=models.CharField(max_length=90)
    filename_real=models.CharField(max_length=90)
    url=models.CharField(max_length=100)


class Backup(models.Model):
    username=models.CharField(max_length=90)
    filename=models.CharField(max_length=90)
    filename_real=models.CharField(max_length=90)
    url=models.CharField(max_length=100)

class SharedFiles(models.Model):
    sender_name=models.CharField(max_length=90)
    receiver_name=models.CharField(max_length=90)
    bucket_name=models.CharField(max_length=90)
    sender_email=models.CharField(max_length=90)
    receiver_email=models.CharField(max_length=90)
    shared_filename=models.CharField(max_length=90)
    real_filename=models.CharField(max_length=90)
