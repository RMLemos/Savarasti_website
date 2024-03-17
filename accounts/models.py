from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Base(models.Model):
    created_at = models.DateField('Created at', auto_now_add=True)
    updated_at = models.DateField('Updated at', auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    class Meta:
        db_table = 'readers'

    reader = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField('Country', max_length=50, null=True, blank=True)
    interests = models.CharField('Interests', max_length=200, null=True, blank=True)
    bio = models.TextField('Profile', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(reader=instance)
