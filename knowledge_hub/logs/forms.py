from django import forms
from django.utils import timezone

from core.forms import BootstrapFormMixin

from .models import LearningLog, Tag, Topic

MAX_TAGS = 10
MAX_TAG_LENGTH = 30


class TopicForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Python"}),
            "description": forms.TextInput(attrs={"placeholder": "Optional short description"}),
        }

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        duplicates = Topic.objects.filter(user=self.user, name__iexact=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("You already have a topic with this name.")
        return name

    def save(self, commit=True):
        topic = super().save(commit=False)
        topic.user = self.user
        if commit:
            topic.save()
        return topic


class LearningLogForm(BootstrapFormMixin, forms.ModelForm):
    tags_text = forms.CharField(
        label="Tags",
        required=False,
        max_length=300,
        help_text="Optional. Separate tags with commas, e.g. django, orm.",
        widget=forms.TextInput(attrs={"placeholder": "django, orm, testing"}),
    )

    field_order = ["title", "topic", "date", "description", "tags_text"]

    class Meta:
        model = LearningLog
        fields = ["title", "topic", "date", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What did you learn?"}),
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "description": forms.Textarea(attrs={"rows": 8}),
        }

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # Users can only pick their own topics.
        self.fields["topic"].queryset = Topic.objects.filter(user=user)
        self.fields["topic"].empty_label = "Choose a topic"
        if self.instance.pk and not self.is_bound:
            self.initial["tags_text"] = ", ".join(t.name for t in self.instance.tags.all())

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > timezone.localdate():
            raise forms.ValidationError("The date cannot be in the future.")
        return date

    def clean_tags_text(self):
        names = []
        for part in self.cleaned_data.get("tags_text", "").split(","):
            name = " ".join(part.split()).lower()
            if not name:
                continue
            if len(name) > MAX_TAG_LENGTH:
                raise forms.ValidationError(
                    f"Each tag must be at most {MAX_TAG_LENGTH} characters long."
                )
            if name not in names:
                names.append(name)
        if len(names) > MAX_TAGS:
            raise forms.ValidationError(f"Use at most {MAX_TAGS} tags.")
        return names

    def save(self, commit=True):
        """Always saves (the log, then its tags), because tags need a saved log."""
        log = super().save(commit=False)
        log.user = self.user
        log.save()
        tags = [
            Tag.objects.get_or_create(user=self.user, name=name)[0]
            for name in self.cleaned_data["tags_text"]
        ]
        log.tags.set(tags)
        # Remove tags that no longer belong to any log.
        Tag.objects.filter(user=self.user, logs__isnull=True).delete()
        return log
