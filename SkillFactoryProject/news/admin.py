from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    list_display = ['title', 'author', 'category', 'created', 'changed']
    list_filter = ['category', 'author', 'created']
    summernote_fields = ('content',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    ordering = ['-created', '-changed']

admin.site.register(Post, PostAdmin)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'category', 'created', 'changed']
#     list_filter = ['category', 'author', 'created']
#     prepopulated_fields = {'slug': ('title',)}
#     raw_id_fields = ['author']
#     ordering = ['-created', '-changed']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'active']
    list_filter = ['active', 'post', 'author']
    raw_id_fields = ['author', 'post']
    ordering = ['-created']
