from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from dateutil.relativedelta import relativedelta
from datetime import datetime

from accounts.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        if instance.is_authenticated:
            assign_perm(
                'change_user',
                instance,
                instance)
            assign_perm(
                'delete_user',
                instance,
                instance)


@receiver(pre_delete, sender=Profile)
def remove_user(sender, instance, created, **kwargs):
    if instance.user:
        instance.user.delete()


@receiver(pre_save, sender=Profile)
def pre_save_profile(sender, instance, **kwargs):
    instance.age = relativedelta(datetime.now(), instance.birth_date).years
