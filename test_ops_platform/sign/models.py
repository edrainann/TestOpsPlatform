from django.db import models


# Create your models here.
class UserModel(models.Model):
    """用户登录信息"""
    username = models.CharField(max_length=50, unique=True)  # 唯一的名字
    password = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)  # 不是必填
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['create_time']  # 按时间排序


class CommonWebsites(models.Model):
    """常用网站的Model"""
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length=300)
    site_description = models.CharField(max_length=50, null=True, blank=True)  # 网站描述，非必填
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name, self.site_url, self.site_description


class CompanyWebsitesOnline(models.Model):
    """公司网站——上线类的Model"""
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length=300)
    site_description = models.CharField(max_length=50, null=True, blank=True)  # 网站描述，非必填
    create_time = models.DateTimeField(auto_now=True)


class SqlSync(models.Model):
    """SQL同步"""
    sql_sync_env = models.CharField(max_length=50)

    def __str__(self):
        return self.sql_sync_env


class EnvironmentName(models.Model):
    """环境名字"""
    env_name = models.CharField(max_length=50)


class ProjectName(models.Model):
    """项目名字"""
    project_name = models.CharField(max_length=50)


class DeployExecuteAction(models.Model):
    """部署执行操作"""
    execute_action = models.CharField(max_length=50)


class Event(models.Model):
    """发布会表"""
    name = models.CharField(max_length=100)  # 发布会标题
    limit = models.IntegerField()  # 参加人数
    status = models.BooleanField()  # 状态
    address = models.CharField(max_length=200)  # 地址
    start_time = models.DateTimeField('event_time')  # 发布会时间
    creat_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.name


class Guest(models.Model):
    """ 嘉宾表"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id
    real_name = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)  # 手机号
    email = models.EmailField()  # 邮箱
    sign = models.BooleanField()  # 签到状态
    creat_time = models.DateTimeField(auto_now=True)  # 创建时间

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.real_name
