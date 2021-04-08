# Generated by Django 3.1.2 on 2021-04-07 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reptile_reg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=64, unique=True, verbose_name='域名')),
                ('url', models.CharField(max_length=64, verbose_name='初始URl')),
                ('FirstReptile', models.DateTimeField(null=True, verbose_name='首次爬取时间')),
                ('LasterReptile', models.DateTimeField(null=True, verbose_name='末次爬取时间')),
                ('pic_number', models.IntegerField(null=True, verbose_name='图片数量')),
                ('text_number', models.IntegerField(null=True, verbose_name='文本数量')),
                ('video_number', models.IntegerField(null=True, verbose_name='视频数量')),
            ],
        ),
    ]