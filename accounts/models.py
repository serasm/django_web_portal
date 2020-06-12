from django import template
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



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
