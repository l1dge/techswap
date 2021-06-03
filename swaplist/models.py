from django.db import models
from django.contrib.auth.models import User


class Wanted(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        "itemmgmt.Location",
        on_delete=models.CASCADE,
    )
    condition_req = models.CharField(max_length=200)
    item_id = models.ForeignKey("itemmgmt.Items", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} {self.location} {self.item_id}"


class ForSwap(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item_id = models.ForeignKey(
        "itemmgmt.Items", related_name="ItemID", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        "itemmgmt.Location",
        on_delete=models.CASCADE,
    )
    swap_avail = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} {self.location} {self.swap_avail}"
