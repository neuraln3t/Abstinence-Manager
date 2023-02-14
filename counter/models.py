from django.db import models
from django.utils import timezone
import datetime
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def default_duration():
    return timezone.timedelta(days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0)

@receiver(post_save, sender=User)
def create_user_abstinence(sender, instance, created, **kwargs):
    if created:
        UserAbstinence.objects.create(user=instance)

class Abstinence(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    is_primary = models.BooleanField(default=False)
    start = models.DateTimeField(default=timezone.now)
    record = models.DurationField(default=default_duration)
    history = models.OneToOneField("History", on_delete=models.DO_NOTHING, null=True)
    trophies = models.ManyToManyField("Trophy", blank=True)

    def __str__(self):
        return str(self.uuid)

class UserAbstinence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    abstinences = models.ManyToManyField(Abstinence, blank=True)
    unchecked_trophies = models.BooleanField(default=False)

class Trophy(models.Model): # Needs setup with predefined trophies in database
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    time_required = models.DurationField()

class History(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entries = models.ManyToManyField("HistoryEntry", blank=True)

class HistoryEntry(models.Model):
    abstinence = models.ForeignKey("Abstinence", on_delete=models.DO_NOTHING, null=True)
    count = models.DurationField(default=default_duration)