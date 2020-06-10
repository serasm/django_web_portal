from django.contrib import admin

from information_page.models import (
    Article,
    ArticleComment,
    ArticleGenre,
    ArticleNote
)


# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(ArticleGenre)
admin.site.register(ArticleNote)