from django.db import models
from django.utils import timezone
import uuid

CATEGORY_CHOICES = (
    ('general_interests', 'General Interests'),
    ('blah', 'Blah'),
)
DAYS = (
    ('1', 'Day 1'),
    ('2', 'Day 2'),
    ('3', 'Day 3'),
    ('4', 'Day 4'),
    ('5', 'Day 5'),
    ('6', 'Day 6'),
    ('7', 'Day 7'),
    ('8', 'Day 8'),
    ('9', 'Day 9'),
    ('10', 'Day 10'),
)


class EmailListSubscriber(models.Model):
    email_sub_name = models.CharField(max_length=255, blank=True, default='')
    user_email = models.EmailField(blank=False)
    is_confirmed = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    emails_sent = models.IntegerField(default=0)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='general_interests')
    random_uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ('-joined',)

    def __str__(self):
        return self.user_email
