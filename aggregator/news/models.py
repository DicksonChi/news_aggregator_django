import uuid
from django.db import models

# Create your models here.

# Create the model for feeds


class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# create the model for Article
class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feed = models.ForeignKey('news.Feed', on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    publication_date = models.DateTimeField()

    class Meta:
        """Extra model properties."""

        ordering = ['-publication_date']

    def __str__(self):
        return self.title
