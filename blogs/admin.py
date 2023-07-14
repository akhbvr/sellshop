from django.contrib import admin

# Custom imports
from blogs.models import (
    Category,
    Tag,
    Post,
    Comment,
)

admin.site.register([Category, Tag, Post, Comment])