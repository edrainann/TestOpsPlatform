import hashlib

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from sign.forms import UserForm
from sign.models import UserModel


# @login_required  # 限制访问
def base_home(request):
    return render(request, 'home/base_home.html')


def sign(request):
    """登录界面"""
    # return render(request, 'sign/sign_in.html')
    user_form = UserForm()
    return render(request, 'sign/sign_in.html', locals())


def login_action(request):
    """执行 登录按钮 操作后的界面"""
    if request.method == 'POST':
        username = request.POST.get('username', '')  # 此处对应表单的form中的input的 name属性
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        # if username == 'qwer' and password == 'qwer':
        if user is not None:
            auth.login(request, user)  # 登录
            # return HttpResponseRedirect(reverse('sign:home'))  # 对路径重定向，成功登陆之后重新指向 /sign/home/ 页面
            request.session['user'] = username  # 将session信息记录到浏览器
            response = HttpResponseRedirect(reverse('sign:home'))
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie,3600的cookie保存时间
            return response
        else:
            return render(request, 'sign/sign_in.html',  # 渲染变量到模板中
                          {'error': 'username or password error!'})  # 返回错误提示的字典{Key:Value}，在index里面添加{error}显示的位置


# @login_required  # 限制访问
def home(request):
    """主页展示"""
    # username = request.COOKIES.get('username', '')  # 读取浏览器cookie
    username = request.session.get('user_name', '')  # 读取浏览器session
    return render(request, "home/home.html", locals())


def sign_up(request):
    """注册"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # 获得表单数据
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            # 添加到数据库
            new_user = UserModel.objects.create()
            new_user.username = username
            new_user.password = hash_code(password)  # 使用加密密码
            new_user.save()
            request.session['is_login'] = True
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.username
            return HttpResponseRedirect(reverse('sign:home'))
    else:
        user_form = UserForm()
    return render(request, 'sign/sign_up.html', locals())


def sign_in(request):
    """登录"""
    user_form = UserForm()
    if request.session.get('is_login', None):  # 不允许重复登录
        return render(request, 'sign/sign_in.html', locals())
    if request.method == "POST":
        user_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if user_form.is_valid():
            # 获取表单信息
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            try:
                # 获取的表单数据与数据库进行比较
                # user = UserModel.objects.filter(username__exact=username, password__exact=password)
                user = UserModel.objects.get(username=username)
                # user = models.User.objects.get(username=username)
                # if user.password == password:
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return HttpResponseRedirect(reverse('sign:home'))
                else:
                    message = "密码不正确"
            except:
                message = "用户不存在"
        return render(request, 'sign/sign_in.html', locals())
    return render(request, 'sign/sign_in.html', locals())
    # if user:
    #     # 比对成功，跳转index
    #     # response = HttpResponseRedirect('/online/index/')
    #     response = HttpResponseRedirect(reverse('sign:home'))
    #     # 将username写入浏览器cookie,失效时间为3600
    #     response.set_cookie('username', username, 3600)
    #     # request.session['username'] = username  # 将session信息记录到浏览器
    #     return response
    # else:
    #     # 比较失败，还在login
    #     # return HttpResponseRedirect('/online/sign_in/')
    #     # return HttpResponseRedirect(reverse('sign'))  # 对路径重定向
    #     message = 'username or password error!'
    #     return render(request, 'sign/sign_in.html', locals())
    #     # 渲染变量到模板中,# 返回错误提示的字典{Key:Value}，在index里面添加{error}显示的位置,
    #     # Python内置了一个locals()函数，它返回当前所有的本地变量字典，将这作为render函数的数据字典参数值，
    #     # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。{'uf': uf,'message': message_info}
    # else:
    #   uf = UserForm()
    #   return render(request, 'sign/sign_in.html', {'uf': uf}) # 最后都要跳转出来，所以省略


def logout(request):
    """注销"""
    # response = HttpResponseRedirect(reverse('sign:sign_in'))
    # # response = HttpResponse('logout !!')
    # # 清理cookie里保存username
    # response.delete_cookie('username')
    # return response
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect(reverse('sign:sign_in'))
    request.session.flush()  # 一次性将session中的所有内容全部清空，确保不留后患
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return HttpResponseRedirect(reverse('sign:sign_in'))


def hash_code(s, salt='edrain'):
    """密码加密，hash"""
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
