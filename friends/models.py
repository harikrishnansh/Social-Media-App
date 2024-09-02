from django.db import models
from users.models import User

# Create your models here.
class FriendRequest(models.Model):
    STATUS_TYPE = (
        (1, 'Pending'),
        (2, 'Accepted'), 
        (3, 'Rejected'),
    )
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default=1)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'friend_request'


class Friends(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='send_user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='recieved_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        managed = True
        db_table = 'friends'