from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
#登陆，注册，修改密码等操作 

#登陆  
class LoginForm(AuthenticationForm):        
    username = UsernameField(
        label = '用户名',
        max_length=20,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )        
    password = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput,
    )
    error_messages = {
        'invalid_login': '',
        'inactive': '',
    }

#注册
from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='请再次输入密码',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {'username':'用户名', 'first_name': '姓名', 'email':'邮箱',}
        help_texts = {'username':'*请输入少于150个字符，只允许输入字母，数字和"@/./+/-/_"'}
        error_messages={'username':{'unique':'该用户名已存在。'},
						'email':{'unique':'该邮箱号已存在。'}}
		
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次输入的密码不相同，请重新输入.')
        return cd['password2']

#个人博客首页

		
#通过邮箱找回密码

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

class CustomPasswordResetForm(PasswordResetForm):
#实现'邮箱未注册'的提示
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email):
            raise forms.ValidationError('邮箱未注册')
        return email

from django.contrib.auth.forms import SetPasswordForm
class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {'password_mismatch':'两次输入的密码不相同，请重新输入'}
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput,
        strip=False,
        help_text='请输入新密码并确认',
    )
    new_password2 = forms.CharField(
        label="确认密码",
        strip=False,
        widget=forms.PasswordInput,
    )

#blog相关功能
#通过email分享帖子
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                                         widget=forms.Textarea)
										 

from .models import Blogpost

class BlogpostEditForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ('title', 'slug', 'body', 'publish',
                    'status')


'''
#blog
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False,
										widget=forms.Textarea)
										


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
		
class SearchForm(forms.Form):
    query = forms.CharField()
'''