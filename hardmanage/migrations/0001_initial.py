# Generated by Django 3.1.2 on 2021-02-04 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=32, unique=True, verbose_name='地址')),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(unique=True, verbose_name='数量')),
            ],
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='CPU型号')),
                ('Core_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='核数', to='hardmanage.count')),
                ('Core_thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='每核线程数', to='hardmanage.count')),
            ],
        ),
        migrations.CreateModel(
            name='Findhard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('IPMASTER', models.GenericIPAddressField(verbose_name='掩码')),
                ('inserttime', models.DateTimeField(auto_now_add=True, verbose_name='登录IP时间')),
                ('mod_date', models.DateTimeField(verbose_name='发现硬件时间')),
            ],
        ),
        migrations.CreateModel(
            name='Frequ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Frequ', models.FloatField(max_length='12', unique=True, verbose_name='频率(MHZ)')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HOSTNAME', models.CharField(max_length=32, unique=True, verbose_name='主机名')),
                ('Serian_Number', models.CharField(max_length=32, unique=True, verbose_name='序列号')),
                ('CPU', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_cpu', to='hardmanage.cpu')),
                ('CPU_NUMber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu_number', to='hardmanage.count', verbose_name='CPU颗数')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='机房名称')),
                ('desflow', models.IntegerField(blank=True, null=True, verbose_name='链路带宽')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addre', to='hardmanage.address', verbose_name='地址')),
                ('host', models.ManyToManyField(related_name='host_idc', to='hardmanage.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Manufacturer', models.CharField(max_length=32, unique=True, verbose_name='生产商')),
            ],
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Size', models.CharField(max_length=32, unique=True, verbose_name='内存大小')),
            ],
        ),
        migrations.CreateModel(
            name='Producer_Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_Name', models.CharField(max_length=32, unique=True, verbose_name='型号')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=32, unique=True, verbose_name='省')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='服务')),
                ('host', models.ManyToManyField(related_name='host_service', to='hardmanage.Host')),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('NETMASK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='掩码', to='hardmanage.count')),
            ],
        ),
        migrations.CreateModel(
            name='IDC_Func',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_func', models.CharField(max_length=32, verbose_name='IDC功能')),
                ('idc', models.ManyToManyField(related_name='idc_func_idc', to='hardmanage.IDC', verbose_name='IDC名称')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='IP',
            field=models.ManyToManyField(related_name='ip_host', to='hardmanage.IP'),
        ),
        migrations.AddField(
            model_name='host',
            name='Manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_modelname', to='hardmanage.manufacturer', verbose_name='生产者'),
        ),
        migrations.AddField(
            model_name='host',
            name='Memory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory_host', to='hardmanage.memory'),
        ),
        migrations.AddField(
            model_name='host',
            name='Memory_Frequ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='内存速率', to='hardmanage.frequ'),
        ),
        migrations.AddField(
            model_name='host',
            name='Memory_NUMber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory_number', to='hardmanage.count'),
        ),
        migrations.AddField(
            model_name='host',
            name='Producer_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardmanage.producer_name', verbose_name='型号'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='Frequ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CPU频率', to='hardmanage.frequ', verbose_name='频率(MHZ)'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32, unique=True, verbose_name='市')),
                ('prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='省', to='hardmanage.province')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='市', to='hardmanage.city'),
        ),
    ]
