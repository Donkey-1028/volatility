from django.contrib import admin
from .models import *


class PostAdminManager(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'update_date')
    list_filter = ('update_date',)


class CommentAdminManager(admin.ModelAdmin):
    list_display = ('author', 'comment')
    list_filter = ('create_date',)


class HitAdmin(admin.ModelAdmin):
    list_display = ('post',)


admin.site.register(Post, PostAdminManager)
admin.site.register(Comment, CommentAdminManager)
admin.site.register(HitCount, HitAdmin)
# Register your models here.
