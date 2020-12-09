from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Score(models.Model):
    score = models.PositiveIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        output = self.user.username + ": " + str(self.score)
        return output
