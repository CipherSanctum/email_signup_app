from django.db import models
import uuid
import random


def random_number():
    return random.randint(1, 50000)


class EmailListPerson(models.Model):
    STATUS_CHOICES = (
        ('unconfirmed', 'Unconfirmed'),
        ('confirmed', 'Confirmed'),
    )
    email = models.CharField(max_length=100)
    status_choices = models.CharField(max_length=30, choices=STATUS_CHOICES, default='unconfirmed')
    random_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    rand_int = models.IntegerField(default=random_number)
    times_downloaded = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'People on list'


class EmailListPersonDelete(models.Model):
    email = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'People requesting to be removed from list'


class EmailCampaign(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)  # Emails are text only for now.
    created = models.DateTimeField(auto_now_add=True)
    start_point = models.IntegerField(default=0)
    end_point = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
