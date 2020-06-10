from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from tools.models import (
    Comment,
    Entry,
    Genre
)
from tools.utils import unique_slug_generator


# Create your models here.
class PostGenre(Genre):

    def get_absolute_url(self):
        return reverse('forum:article-details',
                       kwargs={'slug': self.slug})


class Post(Entry):
    last_edit_date = models.DateTimeField(blank=True, null=True)


class PostComment(Comment):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts_comments')


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, 'title')


def pre_save_genre_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, 'name')


pre_save.connect(pre_save_post_receiver, sender=Post)
pre_save.connect(pre_save_genre_receiver, sender=PostGenre)
