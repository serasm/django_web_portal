from django.contrib.auth.models import User
from django.db import models

from mptt.models import (
    MPTTModel,
    TreeForeignKey
)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    text = models.TextField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Entry(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    slug = models.SlugField(allow_unicode=True, unique=True,
                            editable=False, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Genre(MPTTModel, models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True,
                            editable=False, blank=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='children')

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
