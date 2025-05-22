from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "مرکز"
        verbose_name_plural = "مراکز"

    def __str__(self):
        return self.name

class Channel(models.Model):
    PLATFORM_CHOICES = [
        ('bale', 'bale'),
        ('eitaa', 'eitaa'),
    ]
    name = models.CharField(max_length=100)
    channel_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='allowed_channels', blank=True)

    class Meta:
        verbose_name = "کانال"
        verbose_name_plural = "کانال ها"

    def __str__(self):
        return f"{self.name} ({self.platform}) ({self.channel_id})"


class Post(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to='posts/')
    scheduled_time = models.DateTimeField()
    # scheduled_time = jmodels.jDateTimeField()
    channels = models.ManyToManyField(Channel)
    sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.caption[:20]