from django.contrib import admin
from .models import Category, Post, Tag  

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
# Register your models here.
