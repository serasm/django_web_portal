from django import template
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse

from guardian.shortcuts import assign_perm
from dateutil.relativedelta import relativedelta
from datetime import datetime

register = template.Library()


# Create your models here.
class Profile(models.Model):

    NOTSPECIFIED = 'n'
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = [
        (NOTSPECIFIED, 'Not specified'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=NOTSPECIFIED)
    age = models.IntegerField(editable=False, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile-details',
                       kwargs={'slug': self.slug})
