from django.db import models
from autoslug import AutoSlugField
import uuid
import os


def event_image_file_path(instance, filename):
    """Generate file path for new event image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("event", filename)


class Event(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    host = models.CharField(max_length=50, default="KUASA")
    cover_image = models.ImageField(
        upload_to=event_image_file_path, null=True, blank=True
    )
    slug = AutoSlugField(populate_from="title", unique=True, blank=True)

    def get_absolute_url(self):
        return f"/events/{self.slug}/"
