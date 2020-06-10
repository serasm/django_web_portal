from django.contrib import admin

from forum.models import (
    Post,
    PostComment,
    PostGenre
)


# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostGenre)
