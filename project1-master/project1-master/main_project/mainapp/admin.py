from django.contrib import admin
from . import models
# Register your models here.
class AdminsFiles(admin.ModelAdmin):
    list_display=['username','filename','filename_real','url']

admin.site.register(models.File,AdminsFiles)

class AdminsBackup(admin.ModelAdmin):
    list_display=['username','filename','filename_real','url']

admin.site.register(models.Backup,AdminsBackup)

class AdminsShared(admin.ModelAdmin):
    list_display=['sender_name','receiver_name','bucket_name','sender_email','receiver_email','shared_filename','real_filename']

admin.site.register(models.SharedFiles,AdminsShared)
