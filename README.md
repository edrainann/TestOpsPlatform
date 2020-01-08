# TestOps

## 项目实现功能

1、注册

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/sign_up.png)

2、登录

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/sign_in.png)

3、登录后的主页显示

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/index.png)

4、网站归纳

1）公司网站

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/company_websites_online.png)

2）常用网站

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/common_websites.png)

3）新增网站

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/add_new.gif)

5、项目部署&上线

1）测试环境部署

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/test_env_deploy.png)

2）通过dwebsocket,实现与服务器连接，输入查询指令后，页面的实时滚动

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/test_deploy.gif)

6、SQL同步

![image](https://github.com/edrainann/TestOpsPlatform/raw/master/ReadMe_Photos/sql_sync.png)






## 一、官方文档

Django中文官网: https://docs.djangoproject.com/zh-hans/3.0/

Django英文官网: https://docs.djangoproject.com/en/3.0/

## 二、初始化

### 1、创建项目

使用 startproject 来创建项目

`django-admin startproject edrainsite`

项目显示：

```
test_ops/
    manage.py
    test_ops/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

这些目录和文件的用处是：

- The outer `test_ops/` root directory is a container for your project. Its name doesn't matter to Django; you can rename it to anything you like.
- manage.py: 一个让你用各种方式管理 Django 项目的命令行工具。你可以阅读 django-admin and manage.py 获取所有 manage.py 的细节。
- 里面一层的 test_ops/ 目录包含你的项目，它是一个纯 Python 包。它的名字就是当你引用它内部任何东西时需要用到的 Python 包名。 (比如 test_ops.urls).
- test_ops/__init__.py：一个空文件，告诉 Python 这个目录应该被认为是一个 Python 包。如果你是 Python 初学者，阅读官方文档中的 更多关于包的知识。
- test_ops/settings.py：Django 项目的配置文件。如果你想知道这个文件是如何工作的，请查看 Django 配置 了解细节。
- test_ops/urls.py：Django 项目的 URL 声明，就像你网站的“目录”。阅读 URL调度器 文档来获取更多关于 URL 的内容。
- test_ops/asgi.py: 兼容ASGI的Web服务器为您的项目提供服务的入口点。See How to deploy with ASGI for more details.
- test_ops/wsgi.py：作为你的项目的运行在 WSGI 兼容的Web服务器上的入口。阅读 如何使用 WSGI 进行部署 了解更多细节。

### 2、运行项目

`py manage.py runserver 127.0.0.1:8028`
样就可以运行起来啦 打开网址：http://127.0.0.1:8028/ 进行校验

### 3、创建应用

`py manage.py startapp sign`

这些目录和文件的用处是：

- **migrations/：**用于记录models中数据的变更；
- **admin.py：**映射models中的数据到Django自带的admin后台；
- **apps.py：**用于应用程序的配置（在新的Django版本中新增文件）；
- **models.py：** Django的模型文件，创建应用程序数据表模型（对应数据库的相关操作）；
- **tests.py：**创建Django测试用例；
- **views.py：** Django的视图文件，控制向前段页面显示的内容。

## 三、编写第一个视图

### 1、打开 `sign/views.py`

把下面这些 Python 代码输入进去：

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the sign index.")
```

这是 Django 中最简单的视图。如果想看见效果，我们需要将一个 URL 映射到它——这就是我们需要 URLconf 的原因了。

为了创建 URLconf，请在 sign目录里新建一个 `urls.py` 文件。

### 2、在 sign目录里新建一个 `urls.py` 文件

输入如下代码：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

### 3、在根 URLconf 文件中指定创建的 `sign.urls` 模块

在 `test_ops/urls.py` 文件的 `urlpatterns` 列表里插入一个 `include()`， 如下：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign/', include('sign.urls')),
]
```

函数 [`include()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.include) 允许引用其它 URLconfs。每当 Django 遇到 [`include()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.include) 时，它会截断与此项匹配的 URL 的部分，并将剩余的字符串发送到 URLconf 以供进一步处理。

[`include()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.include) 的理念是使其可以即插即用。因为sign应用有它自己的 URLconf( `sign/urls.py` )，他们能够被放在 "/sign/" ， "/fun_sign/" ，"/content/sign/"，或者其他任何路径下，这个应用都能够正常工作。

> 当包括其它 URL 模式时你应该总是使用 `include()` ， `admin.site.urls` 是唯一例外。



## 四、通过templates来展示页面

### 1、在sign文件夹下面，创建`templates`文件夹

### 2、创建sign.html文件

```html
<html>
    <head>
        <title>Sign</title>
    </head>
    <body>
        <h1>Hello Web!</h1>
    </body>
</html>
```

### 3、修改`sign/urls.py`文件

```python
from django.shortcuts import render


def sign(request):
    # return HttpResponse("Hello, world. You're at the sign index.")
    return render(request, 'sign.html')
```

### 4、修改`settings.py`文件，新增`'sign',`文字

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 你项目的 TEMPLATES 配置项描述了 Django 如何载入和渲染模板。
    # 默认的设置文件设置了 DjangoTemplates 后端，并将 APP_DIRS 设置成了 True。
    # 这一选项将会让 DjangoTemplates 在每个 INSTALLED_APPS 文件夹中寻找 "templates" 子目录。
    'sign',
]
```

你项目的 [`TEMPLATES`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-TEMPLATES) 配置项描述了 Django 如何载入和渲染模板。默认的设置文件设置了 `DjangoTemplates` 后端，并将 [`APP_DIRS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-TEMPLATES-APP_DIRS) 设置成了 True。这一选项将会让 `DjangoTemplates` 在每个 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-INSTALLED_APPS) 文件夹中寻找 "templates" 子目录。这就是为什么尽管我们没有像在第二部分中那样修改 DIRS 设置，Django 也能正确找到 polls 的模板位置的原因。

输入网址：<http://127.0.0.1:8028/sign/>



## 五、数据库配置

Django 提供完善的模型（model）层主要用来创建和存取数据，不需要我们直接对数据库操作。

**Django模型的基础知识：**

- 每个模型是一个Python类，继承**django.db.models.Model类**
- 该模型的每个属性表示一个数据库表字段
- 所有这一切，已经给了你一个自动生成数据库访问的API

### 1、打开 `test_ops/settings.py` ,配置Database

这是个包含了 Django 项目设置的 Python 模块。通常，这个配置文件使用 SQLite 作为默认数据库。如果你不熟悉数据库，或者只是想尝试下 Django，这是最简单的选择。Python 内置 SQLite，所以你无需安装额外东西来使用它。当你开始一个真正的项目时，你可能更倾向使用一个更具扩展性的数据库，例如 PostgreSQL，避免中途切换数据库这个令人头疼的问题。

如果你想使用其他数据库，你需要安装合适的 [database bindings](https://docs.djangoproject.com/zh-hans/3.0/topics/install/#database-installation) ，然后改变设置文件中 [`DATABASES`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-DATABASES) `'default'` 项目中的一些键值：

- [`ENGINE`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-DATABASE-ENGINE) -- 可选值有 `'django.db.backends.sqlite3'`，`'django.db.backends.postgresql'`，`'django.db.backends.mysql'`，或 `'django.db.backends.oracle'`。其它 [可用后端](https://docs.djangoproject.com/zh-hans/3.0/ref/databases/#third-party-notes)。
- [`NAME`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-NAME) - 数据库的名称。如果使用的是 SQLite，数据库将是你电脑上的一个文件，在这种情况下， [`NAME`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-NAME) 应该是此文件的绝对路径，包括文件名。默认值 `os.path.join(BASE_DIR, 'db.sqlite3')` 将会把数据库文件储存在项目的根目录。

```python
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 2、打开 `test_ops/settings.py` ,配置INSTALLED_APPS

`test_ops/settings.py`文件头部的 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-INSTALLED_APPS) 设置项。这里包括了会在你项目中启用的所有 Django 应用。应用能在多个项目中使用，你也可以打包并且发布应用，让别人使用它们。

通常， [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-INSTALLED_APPS) 默认包括了以下 Django 的自带应用：

- [`django.contrib.admin`](https://docs.djangoproject.com/zh-hans/3.0/ref/contrib/admin/#module-django.contrib.admin) -- 管理员站点。
- [`django.contrib.auth`](https://docs.djangoproject.com/zh-hans/3.0/topics/auth/#module-django.contrib.auth) -- 认证授权系统。
- [`django.contrib.contenttypes`](https://docs.djangoproject.com/zh-hans/3.0/ref/contrib/contenttypes/#module-django.contrib.contenttypes) -- 内容类型框架。
- [`django.contrib.sessions`](https://docs.djangoproject.com/zh-hans/3.0/topics/http/sessions/#module-django.contrib.sessions) -- 会话框架。
- [`django.contrib.messages`](https://docs.djangoproject.com/zh-hans/3.0/ref/contrib/messages/#module-django.contrib.messages) -- 消息框架。
- [`django.contrib.staticfiles`](https://docs.djangoproject.com/zh-hans/3.0/ref/contrib/staticfiles/#module-django.contrib.staticfiles) -- 管理静态文件的框架。

这些应用被默认启用是为了给常规项目提供方便。

默认开启的某些应用需要至少一个数据表，所以，在使用他们之前需要在数据库中创建一些表。请执行以下命令：

`...\> py manage.py migrate`

> 就像之前说的，为了方便大多数项目，我们默认激活了一些应用，但并不是每个人都需要它们。如果你不需要某个或某些应用，你可以在运行 [`migrate`](https://docs.djangoproject.com/zh-hans/3.0/ref/django-admin/#django-admin-migrate) 前毫无顾虑地从 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-INSTALLED_APPS) 里注释或者删除掉它们。 [`migrate`](https://docs.djangoproject.com/zh-hans/3.0/ref/django-admin/#django-admin-migrate) 命令只会为在 [`INSTALLED_APPS`](https://docs.djangoproject.com/zh-hans/3.0/ref/settings/#std:setting-INSTALLED_APPS) 里声明了的应用进行数据库迁移。

### 3、创建模型

在sign/models.py文件中，新增

```python

```

### 4、当模型创建好以后，执行数据库迁移

**使用如下命令进行数据库表的初始化和创建（迁移）：**

```
运行 python manage.py makemigrations sign 为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。
```



## 六、认证登录

### 1、创建admin系统用户

`...\> python manage.py createsuperuser`

### 2、输入用户、密码信息

```python
py manage.py createsuperuser

sername (leave blank to use 'edrain'): admin

mail address: admin@mail.com

Password:

assword (again):

his password is too short. It must contain at least 8 characters.

his password is too common.

ypass password validation and create user anyway? [y/N]: y

uperuser created successfully.
```




## 七、开发模式

这段话在Django官方文档也曾出现过：鼓励松耦合以及对应用程序中不同部分的严格分割。

### 1、MVC开发模式
MVC：Model-View-Controller

- model：数据存取层。
- view：表现逻辑，代表的是系统中选择显示什么和怎么显示的部分。
- controller：业务逻辑，代表系统中根据用户输入及需要访问模型，使用哪个视图的哪部分。

对应到Django后：

- Model：数据存取部分，由Django数据库层处理；
- View：表现逻辑，选择显示哪些数据要显示以及怎样显示的部分，由Django的视图和模板处理；
- Controller：业务逻辑，由Django根据URLconf设置，对给定URL调用适当的Python函数。


### 2、MTV开发模式

由于Controller由框架自行处理，而Django里更关注的是模型（Model）、模板（Template）、视图（View），因此Django也被称为MTV框架。

MTV：Model-Template-Views

- Model：模型，数据存取层，该层处理与数据相关的所有事务，即如何存取、如果验证有效等；
- Template：模板，表现层，该层处理与表现相关的所有事务，即如何在页面或者其他类型文档中进行显示；
- View：视图，业务逻辑层，该层包含存取模型及调取恰当模板的相关逻辑，可以看作是模型和模板之间的桥梁。



## 八、小技巧

### 1、去除模板中的硬编码 URL

1）修改`sign/templates/sign/sign_in.html`文件

当发送登录请求时，链接是硬编码的：

`<form action="/login_action/" method="post">`

问题在于，硬编码和强耦合的链接，对于一个包含很多应用的项目来说，修改起来是十分困难的。然而，因为你在 `sign.urls` 的 [`url()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.conf.urls.url) 函数中通过 name 参数为 URL 定义了名字，你可以使用 `{% url %}` 标签代替它。

替代如下：

`<form action="{%  url 'login_action' %}" method="post">`

这个标签的工作方式是在 `sign.urls` 模块的 URL 定义中寻具有指定名字的条目。你可以回忆一下，具有名字 'login_action' 的 URL 是在如下语句中定义的。

2）修改`sign/urls.py`文件，新增`name='login_action'`

`path('login_action/', views.login_action, name='login_action'),  # name的值可以在html中关联{% url 'xxx' %} template tag`

如果你想改变登录视图的 URL，比如想改成 sign/edrain/login_action/ ，你不用在模板里修改任何东西（包括其它模板），只要在`sign/urls.py` 里稍微修改一下就行。

修改如下：

```
# added the word 'edrain'
path('edrain/login_action/', views.login_action, name='login_action'),
```

### 2、为 URL 名称添加命名空间

Django 如何知道 `{% url %}` 标签到底对应哪一个应用的 URL 呢？

1）在根 URLconf 中添加命名空间。在 `sign/urls.py` 文件中稍作修改，加上 `app_name` 设置命名空间：

​```python
from django.urls import path

from . import views

app_name = 'sign'  # 设置命名空间
urlpatterns = [
    path('', views.sign, name='sign'),
    path('login_action/', views.login_action, name='login_action'),  # name的值可以在html中关联{% url 'xxx' %} template tag
]
```

2）修改sign/templates/sign/sign_in.html文件,

从`<form action="{%  url 'login_action' %}" method="post">`

修改为指向具有命名空间的详细视图，变更为：

`<form action="{%  url 'sign:login_action' %}" method="post">`

### 3、HttpReponseDirect使用软编码链接

硬编码链接：可以通过使用HttpResponseRedirect('/index/?page=2')直接获取第2页的文章列表

HttpReponseDirect只支持hard coded urls(硬编码链接), 不能直接使用命名的URL，如使用HttpResponseDirect('blog:article_list‘)是错误的。

在使用URL命名时，我们需要先通过URL反向解析方法reverse先对命名URL(article_list)进行解析，然后再使用HttpReponseRedirect定向(如下面的代码)。背后的逻辑是reverse('blog:article_list')='/index/'。

​```python
def login_action(request):
    """执行 登录按钮 操作后的界面"""
    if request.method == 'POST':
        username = request.POST.get('username', '')  # 此处对应表单的form中的input的 name属性
        password = request.POST.get('password', '')
        if username == 'qwer' and password == 'qwer':
            return HttpResponseRedirect(reverse('sign:home'))  # 对路径重定向，成功登陆之后重新指向 /sign/home/ 页面
```

链接：https://blog.csdn.net/weixin_42134789/article/details/81505963

## 九、疑问

### Q1：db.sqlite3是什么？

A1：链接：<https://www.runoob.com/sqlite/sqlite-intro.html>

SQLite是一个进程内的库，实现了自给自足的、无服务器的、零配置的、事务性的 SQL 数据库引擎。它是一个零配置的数据库，这意味着与其他数据库一样，您不需要在系统中配置。就像其他数据库，SQLite 引擎不是一个独立的进程，可以按应用程序需求进行静态或动态连接。SQLite 直接访问其存储文件。

### Q2:项目和应用区别？

A2：链接：<https://docs.djangoproject.com/zh-hans/3.0/intro/tutorial01/>

应用程序是执行某项操作的Web应用程序，例如Weblog系统，公共记录数据库或小型民意调查应用程序。

项目是特定网站的配置和应用程序的集合。一个项目可以包含多个应用程序。一个应用程序可以在多个项目中。

### Q3：Pycharm提示“Unresolved attribute reference 'objects' for class 'UserModel'”

A3：You need to enable Django support. Go to

> **PyCharm -> Preferences -> Languages & Frameworks -> Django**

and then check *Enable Django Support*

### Q4：USE_TZ时区问题

> **datetime.datetime.now()、datetime.datetime.utcnow()与django.util.timezone.now()的区别**

datetime.datetime.now()：
输出的永远是本地时间（naive time）与配置无任任何关系。

datetime.datetime.utcnow()：
如果setting中配置USE_TZ=True则输出的是UTC时间（naive time）;如果setting中配置USE_TZ=False，则该输出时间与datetime.datetime.now()完全相同。

django.util.timezone.now()：
如果setting中配置USE_TZ=True则输出的是UTC时间（active time），如果配置USE_TZ=False，则与datetime.datetime.now()完全相同。