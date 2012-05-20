from django.db import models

from django.contrib.auth.models import User

BLOG = 'blog'
GROUP = 'group'

class Comment(models.Model):
    author = models.ForeignKey(User)
    thing_id = models.IntegerField(blank=False, null=False)
    parent_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(max_length=10000, null=False)
    type = models.CharField(max_length=20)
    num_edits = models.IntegerField(max_length=100, default=0, null=True, blank=True)
    is_active = models.BooleanField(default=1, null=False, blank=False)

    ups = models.IntegerField(default=0, blank=True, null=True)
    downs = models.IntegerField(default=0, blank=True, null=True)

    thread_id = models.CharField(max_length=100, null=False, blank=False)
    reverse_thread_id = models.CharField(max_length=100, null=False, blank=False)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    MAXIMUM_NESTS = 15

    def nestCount(self):
        return self.thread_id.count('.')
