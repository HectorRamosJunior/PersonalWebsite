from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


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
    retwoot_count = models.IntegerField(default=0)
    notification_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

    def get_retwoot_pks(self):
        return set(self.retwoots.values_list('twoot', flat=True))

    def get_favorite_pks(self):
        return set(self.favorites.values_list('twoot', flat=True))

    def __unicode__(self):
        return self.user.username


class Twoot(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="twoots")
    creation_date = models.DateTimeField(auto_now_add=True)

    favorite_count = models.IntegerField(default=0)
    retwoot_count = models.IntegerField(default=0)

    text = models.CharField(max_length=140, null=False, blank=False)

    def __unicode__(self):
        return (self.twotter_profile.user.username + " twooted: " + self.text)


class Favorite(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="favorites")
    twoot = models.ForeignKey(Twoot, related_name="favorites")

    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.twotter_profile.user.username + " favorited: " + self.twoot.text)


class ReTwoot(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="retwoots")
    twoot = models.ForeignKey(Twoot, related_name="retwoots")

    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.twotter_profile.user.username + " retwooted: " + self.twoot.text)


class Notification(models.Model):
    twotter_profile = models.ForeignKey(TwotterProfile, related_name="notifications")
    notifier_profile = models.ForeignKey(TwotterProfile)

    action = models.CharField(max_length=20)
    twoot = models.ForeignKey(Twoot)

    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.notifier_profile.user.username + " " + self.action + " " + 
                self.twotter_profile.user.username + "'s twoot: " + self.twoot.text)