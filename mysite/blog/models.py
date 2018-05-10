
# Create your models here.


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings



class BlogPostOpenManager(models.Manager):
    def get_queryset(self):
        return super(BlogPostOpenManager,
                    self).get_queryset().filter(status='open')

class BlogPostHiddenManager(models.Manager):
    def get_queryset(self):
        return super(BlogPostHiddenManager,
                    self).get_queryset().filter(status='hidden')
    

class Blogpost(models.Model):
    
    author = models.ForeignKey(User,related_name='blog_posts',
                                on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('hidden', '私密'),
        ('open', '公开'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='hidden')
    objects = models.Manager()
    opened = BlogPostOpenManager()
    hiddened = BlogPostHiddenManager()
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail',
                        args=[self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              self.slug])
    def get_absolute_post(self):
        return reverse('edit_post',
                        args=[self.slug,
                              self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              
                              ])
    def del_absolute_post(self):
        return reverse('del_post',
                        args=[self.slug,
                              self.publish.strftime('%d'),
                              self.publish.strftime('%m'),
                              self.publish.year,
                              ])
							  
							  

    
