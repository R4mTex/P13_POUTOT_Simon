from django.contrib import admin
from blog.models import Blog, Favorite

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')

@admin.register(Favorite)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog')