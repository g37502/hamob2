from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from hardmanage.models import IDC


class Domain(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(verbose_name='域名',unique=True, max_length=255, blank=True, null=True)
    catchdate = models.DateField(blank=True, null=True)
    ischeck = models.BooleanField(blank=True, null=True)
    endcatchdate = models.DateField(verbose_name='最后一次中标时间',blank=True, null=True)
    domaintype = models.BooleanField(blank=True, null=True)
    insertdate = models.DateField(blank=True, null=True)
    accpoint = models.CharField(max_length=1, blank=True, null=True)
    sendtime = models.DateTimeField(blank=True, null=True)
    lastsendtime = models.DateField(blank=True, null=True)
    pv = models.FloatField(blank=True, null=True)
    protocolid = models.CharField(max_length=4, blank=True, null=True)
    iswhite = models.CharField(max_length=1, blank=True, null=True)
    crawlflag = models.BooleanField(blank=True, null=True)
    domainflag = models.BooleanField(blank=True, null=True)
    phishing_flag_type = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domain'
        app_label = 'business_presen'
class DqPic(models.Model):
    id = models.BigIntegerField(blank=True, null=True)
    domainid = models.ForeignKey(Domain, on_delete=models.DO_NOTHING, db_column='domainid')
    catchdate = models.DateField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    pichash = models.CharField(max_length=100, blank=True, null=True)
    picpv = models.BigIntegerField(blank=True, null=True)
    colleteid = models.CharField(max_length=100, blank=True, null=True)
    protocolid = models.CharField(max_length=4, blank=True, null=True)
    referurl = models.CharField(max_length=4000, blank=True, null=True)
    cookiefile = models.CharField(max_length=64, blank=True, null=True)
    sendtime = models.DateTimeField(blank=True, null=True)
    insertdate = models.DateField(blank=True, null=True)
    pic_id = models.CharField(max_length=100, blank=True, null=True)
    pic_id_similarty = models.IntegerField(blank=True, null=True)
    phishing_similarity = models.IntegerField(blank=True, null=True)
    picdimen = models.BigIntegerField(blank=True, null=True)
    phishingpicid = models.BigIntegerField(blank=True, null=True)
    ip = models.CharField(max_length=64, blank=True, null=True)
    port = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dq_pic'
        app_label = 'orac119'
        # app_label = 'business_presen'

class b_info(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    MonitorAdress = models.CharField(max_length=32)
    DesFlow = models.IntegerField()

class Count_mon(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    Monitor = models.BigIntegerField()
    filescount = models.IntegerField()
    reportURLNUM =models.IntegerField()
    monitorURLNUM = models.BigIntegerField()
    inserttime = models.DateField()
    MonitorAddress = models.ForeignKey(IDC,on_delete=models.CASCADE,related_name='count_mon_idc')

class Count_data(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    Monitor = models.BigIntegerField(verbose_name='流量')
    filescount = models.IntegerField()
    reportURLNUM =models.IntegerField(verbose_name='疑似量')
    monitorURLNUM = models.BigIntegerField(verbose_name='URL数量')
    inserttime = models.DateTimeField()
    MonitorAddress = models.ForeignKey(IDC, on_delete=models.CASCADE)






