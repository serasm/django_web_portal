from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from guardian.shortcuts import assign_perm

from tools.models import (
    Comment,
    Entry,
    Genre
)
from tools.utils import unique_slug_generator


# Create your models here.
class ArticleGenre(Genre):

    def get_absolute_url(self):
        return reverse('informations:genre-details',
                       kwargs={'slug': self.slug})

    def publicated_articles(self):
        return self.article_set.filter(published=True).count()


class Article(Entry):
    genre = models.ForeignKey(ArticleGenre,
                              on_delete=models.CASCADE)
    last_modification_date = models.DateTimeField(blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('can_publish', 'Can publish article'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.published:
            self.publication_date = datetime.now()
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.slug})

    def publish(self):
        self.publication_date = datetime.now()
        self.published = True
        self.save()


class ArticleComment(Comment):
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments',
                                editable=False)

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.article.slug})


class ArticleNote(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.article.slug})


@receiver(pre_save, sender=Article)
def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, 'title')


@receiver(post_save, sender=Article)
def post_save_article(sender, **kwargs):
    instance, created = kwargs['instance'], kwargs['created']
    if created and instance.author.is_authenticated:
        editors = User.objects.exclude(
            username__iexact=instance.author.username).filter(
            groups__name__iexact='editors')
        assign_perm(
            'information_page.can_publish',
            editors,
            instance)
        assign_perm(
            'information_page.change_article',
            instance.author,
            instance
        )
        assign_perm(
            'information_page.delete_article',
            instance.author,
            instance
        )


@receiver(pre_save, sender=ArticleGenre)
def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, 'name')


@receiver(post_save, sender=ArticleComment)
def post_save_comment_receiver(sender, **kwargs):
    instance, created = kwargs['instance'], kwargs['created']
    if created and instance.author.is_authenticated:
        assign_perm(
            'change_articlecomment',
            instance.author,
            instance)
        assign_perm(
            'delete_articlecomment',
            instance.author,
            instance)


@receiver(post_save, sender=ArticleNote)
def post_save_note_receiver(sender, **kwargs):
    instance, created = kwargs['instance'], kwargs['created']
    if created and instance.author.is_authenticated:
        assign_perm(
            'change_articlenote',
            instance.author,
            instance)
        assign_perm(
            'delete_articlenote',
            instance.author,
            instance)
