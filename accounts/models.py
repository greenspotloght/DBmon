from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class company_admin(models.Model):
    company_name = models.CharField(max_length=30, verbose_name='公司名稱')
    company_id = models.CharField(unique=True, verbose_name='公司統編', max_length=8)
    company_tel = models.CharField(max_length=20, verbose_name='公司電話', null=True, blank=True)
    company_fax = models.IntegerField(verbose_name='公司傳真', null=True, blank=True)
    company_ip = models.GenericIPAddressField(verbose_name='公司IP位址', unique=True)
    company_ip2 = models.GenericIPAddressField(verbose_name='公司IP位址2', unique=True, null=True, blank=True)
    company_ip3 = models.GenericIPAddressField(verbose_name='公司IP位址3', unique=True, null=True, blank=True)
    company_address = models.TextField(verbose_name='公司地址')
    company_db = models.CharField(max_length=12, verbose_name='公司資料庫', null=True, blank=True)
    principal = models.ForeignKey(User, verbose_name='公司帳戶管理帳戶', null=True, blank=True)
    date_joined = models.DateField(verbose_name='加入日期', auto_now_add=True)
    date_expiration = models.DateField(verbose_name='有效日期', blank=True)
    is_active = models.BooleanField(verbose_name='使用中', blank=True)
    line_group_id = models.CharField(verbose_name='Line群組ID', max_length=33, blank=True, null=True)#, unique=True)

    class Meta:
        db_table = 'Company_Admin'
        verbose_name = '公司資訊'
        verbose_name_plural = '公司資訊'

    def __str__(self):
        return self.company_name


class company_user(models.Model):
    username = models.CharField(max_length=30, verbose_name='使用者帳戶')
    company_admin = models.ForeignKey(company_admin, verbose_name='所屬公司')
    user = models.ForeignKey(User, verbose_name='使用者')
    line_user_id = models.CharField(verbose_name='Line使用者ID', max_length=33, blank=True, null=True)#, unique=True)

    class Meta:
        db_table = 'Company_User'
        verbose_name = '公司與使用者'
        verbose_name_plural = '公司與使用者'

    def __str__(self):
        return self.company_admin + self.user
        #return self.user_id


class User_Verify(models.Model):
    user = models.ForeignKey(User, verbose_name='使用者')
    captcha = models.CharField(max_length=6, verbose_name='認證碼')
    is_verify = models.BooleanField(default=0, verbose_name='已認證')

    class Meta:
        db_table = 'User_Verify'
        verbose_name = '使用者認證'
        verbose_name_plural = '使用者認證'

    def __str__(self):
        return self.user



class suggestion(models.Model):
    user = models.ForeignKey(User, verbose_name='使用者')
    title = models.CharField(max_length=50, verbose_name='主旨')
    suggestion = models.TextField(verbose_name='建議')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suggestion'
        verbose_name = '意見回饋'
        verbose_name_plural = '意見回饋'


class temp_pass(models.Model):
    user = models.ForeignKey(User, verbose_name='使用者',unique=True)
    temp = models.CharField(max_length=6, verbose_name='暫時密碼',unique=True)
    expiration = models.DateTimeField(verbose_name='有效日期', blank=True)

    class Meta:
        db_table = 'Temp_Pass'
        verbose_name = '暫時密碼'
        verbose_name_plural = '使用者暫時密碼'

    def __str__(self):
        return self.user
