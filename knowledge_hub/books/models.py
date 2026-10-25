from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Book(models.Model):
    class Status(models.TextChoices):
        TO_READ = "to_read", "To Read"
        READING = "reading", "Reading"
        COMPLETED = "completed", "Completed"

    CATEGORY_SUGGESTIONS = [
        "Technology", "Science", "Business", "Self-help", "Fiction",
        "Non-fiction", "History", "Biography", "Other",
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books"
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=60, default="Other")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.TO_READ)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"pk": self.pk})

    @property
    def star_range(self):
        return range(1, 6)
