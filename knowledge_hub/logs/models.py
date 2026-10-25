from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Topic(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="topics"
    )
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_topic_per_user"),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_tag_per_user"),
        ]

    def __str__(self):
        return self.name


class LearningLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_logs"
    )
    title = models.CharField(max_length=150)
    # PROTECT: a topic that still has logs cannot be deleted by accident.
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="logs")
    description = models.TextField()
    date = models.DateField(default=timezone.localdate)
    tags = models.ManyToManyField(Tag, blank=True, related_name="logs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("logs:detail", kwargs={"pk": self.pk})
