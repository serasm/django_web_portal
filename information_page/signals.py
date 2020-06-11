from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm
from tools.utils import unique_slug_generator

from information_page.models import (
    Article,
    ArticleGenre,
    ArticleComment,
    ArticleNote
)


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
