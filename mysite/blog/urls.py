from django.conf.urls import url
from django.contrib.auth.views import login
# With django 1.10 I need to pass the callable instead of 
# url(r'^login/$', 'django.contrib.auth.views.login', name='login')

from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # post views
    # login logout
    url(r'^$',views.PostListView.as_view(), name='blog'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    # change password
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    # reset password
    ## restore password urls
    url(r'^password-reset/$',
        views.CustomPasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset/done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    #register
    url(r'^register/$', views.register, name='register'),
    #blog
    url(r'^blog/$', views.PostListView.as_view(), name='blog'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
		#用@login_required装饰myblog页面，登录才能看到
    #url(r'^myblog/$',login_required(views.BlogListView.as_view()), name='myblog'),
    url(r'^myblog/$',views.myblog, name='myblog'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^(?P<post>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$'
        , views.edit_post, name='edit_post'),
    url(r'^(?P<post>[-\w]+)/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$'
        , views.del_post, name='del_post'),
    ]