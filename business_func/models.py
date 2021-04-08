from django.db import models

# Create your models here.

class Reptile_reg(models.Model):
    domain = models.CharField(max_length=64, verbose_name="域名",unique=True)
    url = models.CharField(max_length=256, verbose_name="初始URl",)
    FirstReptile=models.DateTimeField(verbose_name="首次爬取时间",null=True)
    LasterReptile=models.DateTimeField(verbose_name="末次爬取时间",null=True)
    pic_number=models.IntegerField(verbose_name="图片数量",null=True)
    text_number=models.IntegerField(verbose_name='文本数量',null=True)
    video_number=models.IntegerField(verbose_name="视频数量",null=True)

