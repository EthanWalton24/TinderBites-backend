from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Group(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True, default='Group')
    address = models.TextField(max_length=500, blank=True, null=True)
    radius = models.DecimalField(max_digits=7, decimal_places=2) #in miles (0-24.85) meter=miles*1609.34
    limit = models.SmallIntegerField(default=50) #0-50
    places = models.JSONField(default=list, blank=True, null=True)
    swipes = models.JSONField(default=dict, blank=True, null=True)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)



#create/update person on user create/update
@receiver(post_save, sender=User)
def create_user_person(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_person(sender, instance, **kwargs):
    instance.person.save()