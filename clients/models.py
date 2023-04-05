from django.db import models
from users.models import CustomUser

class UserClients(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='user')
    client = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='client')
    discount = models.IntegerField()
    blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'client')
