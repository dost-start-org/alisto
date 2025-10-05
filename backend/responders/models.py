from django.db import models
from django.conf import settings
import uuid

class Responder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agency = models.ForeignKey('agencies.Agency', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'agency')

    def __str__(self):
        return f"{self.user.email} - {self.agency.name}"