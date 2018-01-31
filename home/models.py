from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from stream_django.activity import Activity


# Create your models here.

class FeedModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField()
    like = models.IntegerField(default=0)
    dateTime = models.DateTimeField(auto_now=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, related_name='photofeed')

    def get_absolute_url(self):
        u=self.user
        return reverse('home:feed',u.primary_key)



class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.user


class ExtraInfoUser(models.Model):
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows", default=0)
    following = models.ForeignKey(User, related_name="followed_by", default=0)


    def __str__(self):
        return self.following.username

    def __unicode__(self):
        return self.following


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", default=0)
    feedmodel = models.ForeignKey(FeedModel, default=0)

