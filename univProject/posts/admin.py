from django.contrib import admin
from .models import Post, PostLike, PostCheer, Comment

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostCheer)
admin.site.register(Comment)