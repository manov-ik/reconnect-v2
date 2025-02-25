from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Interest(models.Model):
    field1 = models.CharField(max_length=100, blank=True, null=True)
    field2 = models.CharField(max_length=100, blank=True, null=True)
    field3 = models.CharField(max_length=100, blank=True, null=True)
    field4 = models.CharField(max_length=100, blank=True, null=True)
    field5 = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.roll_no

class CustomUser(AbstractUser):
    ph_no = models.CharField(max_length=15, unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    dept = models.CharField(max_length=100)
    interest = models.ForeignKey(Interest, on_delete=models.SET_NULL, null=True, blank=True)
    
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    class Meta:
        app_label = 'main'  # Change this from 'auth' to 'main'

class UserGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class GroupUser(models.Model):
    grp = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    grp = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status = models.CharField(max_length=50, default="sent")
    media_url = models.URLField(blank=True, null=True)

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    media_url = models.URLField(blank=True, null=True)
    event_description = models.TextField()
    event_reg_link = models.URLField(blank=True, null=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
