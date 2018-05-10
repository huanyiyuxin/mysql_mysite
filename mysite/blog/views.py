from django.http import HttpResponse
from django.contrib.sessions.models import Session# Create your views here.  
from django.shortcuts import render,redirect,get_object_or_404    
from django.contrib.auth import authenticate, login    
from .forms import LoginForm
#验证用户是否登录



#1.登陆，注册，修改密码，重置密码等
#登陆

from django.contrib.auth.views import LoginView

class Login(LoginView):
    form_class = LoginForm
    

#注册 

from .forms import LoginForm, UserRegistrationForm
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                         'registration/register_done.html',
                         {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                 'registration/register.html',
                 {'user_form': user_form})
				 

#通过email重置密码
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
	
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomSetPasswordForm
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

#2.blog
#公共博客首页
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Blogpost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def blog(request):
    object_list = Blogpost.opened.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/blog.html',
                  {'page': page, 
                   'posts': posts})
from django.views.generic import ListView
#使用Django提供的通用ListView使的blog视图（view）转变为一个基于类的视图。这个基础视图（view）允许对任意的对象进行排列。

class PostListView(ListView):
    queryset = Blogpost.opened.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/blog.html'
	
#帖子详情页
def post_detail(request, year, month, day, post):

    post = get_object_or_404(Blogpost, 
                            publish__startswith=year+'-'+month+'-'+day,
#                            publish__year=year,
#                            publish__month=month,
#                            publish__day=day,
                            slug=post)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

				  
				  
				  
from .forms import BlogpostEditForm
@login_required
def add_post(request):
    if request.method =='POST':
        new_post = Blogpost(author=request.user)
        post_form = BlogpostEditForm(request.POST,instance=new_post)#instance=new_post是把post_form中的request.POST获取的值赋值给new_post
        post_form.save()
        if not post_form.is_valid():
            return HttpResponse('您的输入有误，请重新输入')
        else:
            return redirect('myblog')
    else:
        post_form = BlogpostEditForm()
    return render(request,
                  'blog/post/add_post.html',
                  {'post_form':post_form})
				  
				  

def edit_post(request, year, month, day, post):

    if request.method =='POST':
        post = get_object_or_404(Blogpost, slug=post,
                                    publish__startswith=year+'-'+month+'-'+day)
#                                   publish__year=year,
#                                   publish__month=month,
#                                   publish__day=day)
        post_form = BlogpostEditForm(request.POST,instance=post)#instance=new_post是把post_form中的request.POST获取的值赋值给new_post
        post_form.save()
        if not post_form.is_valid():
            return HttpResponse('您的输入有误，请重新输入')
        else:
            return redirect('myblog')
    else:
        post = get_object_or_404(Blogpost, slug=post,
                                    publish__startswith=year+'-'+month+'-'+day)
#                                   publish__year=year,
#                                   publish__month=month,
#                                   publish__day=day)
        post_form = BlogpostEditForm({'title':post.title,'slug':post.slug,'body':post.body,'publish':post.publish,'status':post.status},instance=post)
    return render(request,
                  'blog/post/edit_post.html',
                  {'post':post,'post_form':post_form})


def del_post(request,post, year, month, day ):

    post = get_object_or_404(Blogpost, slug=post,
                                    publish__startswith=year+'-'+month+'-'+day)#mysql写法
#                             publish__day=day,
#                             publish__month=month,#sqlite3写法
#                             publish__year=year,
#                             )
    Blogpost.objects.get(slug=post.slug).delete()
    return redirect('myblog')

#个人博客首页
#myblog
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
@login_required
#用Django内置的Paginator类管理分页。
def myblog(request):
    #查询当前登录的用户名
    username = request.user.username
    #在数据库中搜索该用户名发布的所有帖子
    post_list = Blogpost.objects.all()
    blog_post_list = []
    for num in range(0,len(post_list)):
        if post_list[num].author.username == username:
            blog_post_list.append(post_list[num])
    paginator = Paginator(blog_post_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/myblog.html',
                  {'page': page, 
                   'posts': posts})

from django.contrib.auth.models import User
class BlogListView(ListView):
    
    queryset = Blogpost.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/myblog.html'




#通过email分享帖子
from .forms import EmailPostForm

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostform()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})

													
													

				  
				  
				  
