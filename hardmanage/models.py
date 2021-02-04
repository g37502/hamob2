from django.db import models

# Create your models here.
class Findhard(models.Model):
    IP=models.GenericIPAddressField(verbose_name="IP地址",unique=True)
    IPMASTER = models.GenericIPAddressField(verbose_name="掩码")
    inserttime= models.DateTimeField(verbose_name='登录IP时间',auto_now_add=True)
    mod_date = models.DateTimeField(verbose_name="发现硬件时间")
class Count(models.Model):
    count = models.IntegerField(verbose_name='数量',unique=True)
    def __str__(self):
        return str(self.count)
class Frequ(models.Model):
    Frequ = models.FloatField(verbose_name='频率(MHZ)',max_length='12',unique=True)
    def __str__(self):
        return str(self.Frequ)
class CPU(models.Model):
    name = models.CharField(verbose_name='CPU型号',unique=True,max_length=64)
    Core_number = models.ForeignKey(Count, on_delete=models.CASCADE, related_name='核数')
    Frequ = models.ForeignKey(Frequ, on_delete=models.CASCADE, related_name='CPU频率',verbose_name='频率(MHZ)')
    Core_thread=models.ForeignKey(Count,on_delete=models.CASCADE, related_name='每核线程数')
    def __str__(self):
        return self.name
class Manufacturer(models.Model):
    Manufacturer = models.CharField(verbose_name='生产商', max_length=32,unique=True)
    def __str__(self):
        return self.Manufacturer
class Producer_Name(models.Model):
    Product_Name = models.CharField(verbose_name='型号', max_length=32,unique=True)
    def __str__(self):
        return self.Product_Name
class Memory(models.Model):
    Size = models.CharField(verbose_name="内存大小",unique=True,max_length=32)
    def __str__(self):
        return self.Size
class IP(models.Model):
    IP = models.GenericIPAddressField(verbose_name='IP地址',unique=True)
    NETMASK = models.ForeignKey(Count,on_delete=models.CASCADE,related_name='掩码')
    def __str__(self):
        return self.IP
class Host(models.Model):
    HOSTNAME=models.CharField(verbose_name='主机名',max_length=32,unique=True)
    Serian_Number = models.CharField(verbose_name='序列号',max_length=32,unique=True)
    Producer_Name = models.ForeignKey(Producer_Name,on_delete=models.CASCADE,verbose_name='型号')
    Manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE,related_name='host_modelname',verbose_name='生产者')
    CPU = models.ForeignKey(CPU,on_delete=models.CASCADE,related_name='host_cpu')
    CPU_NUMber = models.ForeignKey(Count,on_delete=models.CASCADE,related_name='cpu_number',verbose_name='CPU颗数')
    Memory = models.ForeignKey(Memory,on_delete=models.CASCADE,related_name='memory_host')
    Memory_Frequ=models.ForeignKey(Frequ,on_delete=models.CASCADE,related_name='内存速率',null=True)
    Memory_NUMber = models.ForeignKey(Count,on_delete=models.CASCADE,related_name='memory_number')
    IP = models.ManyToManyField(IP,related_name='ip_host')
    def __str__(self):
        return self.HOSTNAME
class Province(models.Model):
    province = models.CharField(verbose_name='省', max_length=32, unique=True)
    def __str__(self):
        return self.province
class City(models.Model):
    city = models.CharField(verbose_name='市', max_length=32, unique=True)
    prov = models.ForeignKey(Province, related_name='省', on_delete=models.CASCADE)
    def __str__(self):
        return self.city
class Address(models.Model):
    address = models.CharField(verbose_name='地址', max_length=32, unique=True)
    city = models.ForeignKey(City, related_name='市', on_delete=models.CASCADE)
    def __str__(self):
        return self.address
class IDC(models.Model):
    name = models.CharField(verbose_name='机房名称', max_length=32, unique=True)
    desflow = models.IntegerField(verbose_name='链路带宽',blank=True, null=True)
    address = models.ForeignKey(Address, related_name='addre', verbose_name='地址', on_delete=models.CASCADE)
    host = models.ManyToManyField(Host, related_name='host_idc')
    def __str__(self):
        return self.name
class Services(models.Model):
    name = models.CharField(verbose_name="服务", max_length=32, unique=True)
    host = models.ManyToManyField(Host, related_name='host_service')
    def __str__(self):
        return self.name
class IDC_Func(models.Model):
    name_func = models.CharField(verbose_name='IDC功能', max_length=32)
    idc = models.ManyToManyField(IDC, verbose_name='IDC名称', related_name='idc_func_idc')