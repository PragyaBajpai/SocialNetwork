from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FriendRequest(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "AC", "Active"
        PENDING = "PD", "Pending"
        REJECTED = "RJ", "Rejected"

    from_user = models.ForeignKey(
        User, related_name="sent_friend_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_friend_requests", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )

    class Meta:
        unique_together = ("from_user", "to_user")
