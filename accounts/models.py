from django.db import models


class SocialToken(models.Model):
    access_token = models.CharField(null=True, max_length=100)
