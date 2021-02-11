from django.contrib import admin

from blog.models import Post, Image


class ImageInLine(admin.TabularInline):
    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created']
    inlines = [ImageInLine]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
