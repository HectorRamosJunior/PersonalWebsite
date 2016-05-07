from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class TwotterProfile(models.Model):
    user = models.OneToOneField(User, related_name='twotter_profile')
    creation_date = models.DateTimeField(auto_now_add=True)

    display_name = models.CharField(max_length=25)
    description = models.CharField(max_length=50, default="Not Set Yet")
    location = models.CharField(max_length=25, default="Not Set Yet")
    birthday = models.CharField(max_length=25, default="Not Set Yet")
    avatar_url = models.URLField(default='', blank=True)
    background_url = models.URLField(default='', blank=True)

    twoot_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

    def __unicode__(self):
        return self.user.username


class Twoot(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="twoots")
    creation_date = models.DateTimeField(auto_now_add=True)

    favorite_count = models.IntegerField(default=0)
    #retwoot_count = models.IntegerField(default=0)

    text = models.CharField(max_length=140, null=False, blank=False)

    def __unicode__(self):
        return self.text


class Favorite(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="favorites")
    twoot = models.ForeignKey(Twoot, related_name="favorites")

    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.twotter_profile.user.username


class ReTwoot(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="retwoots")
    twoot = models.ForeignKey(Twoot, related_name="retwoots")

    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.twotter_profile.user.username