from django.db import models, IntegrityError
from django.contrib.auth.models import User

from common.utils import SlugifyUniquely

class Blog(models.Model):
    # Statuses
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3

    statuses = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS,'Hidden'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    status = models.IntegerField(choices=statuses, default=LIVE_STATUS)
    author = models.ForeignKey(User)

    created_ts = models.DateTimeField(auto_now=True, editable=False)
    modified_ts = models.DateTimeField(auto_now_add=True, editable=False)
    # Set this manually when draft->live is implemented
    published_ts = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = SlugifyUniquely(self.title, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
