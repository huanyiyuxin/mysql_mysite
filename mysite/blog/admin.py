from django.contrib import admin

from .models import Blogpost
class BlogpostAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'slug', 'author', 'publish',
                    'status')
    list_filter = ('status', 'created', 'publish', 'author')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
admin.site.register(Blogpost,BlogpostAdmin)