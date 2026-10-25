from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import LearningLog, Tag, Topic

User = get_user_model()


class LogOwnershipTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="S3cure-pass!")
        self.bob = User.objects.create_user("bob", password="S3cure-pass!")
        self.topic = Topic.objects.create(user=self.alice, name="Python")
        self.log = LearningLog.objects.create(
            user=self.alice, title="Decorators", topic=self.topic, description="Notes"
        )

    def test_login_required(self):
        response = self.client.get(reverse("logs:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_other_user_gets_404(self):
        self.client.login(username="bob", password="S3cure-pass!")
        for name in ("detail", "edit", "delete"):
            response = self.client.get(reverse(f"logs:{name}", args=[self.log.pk]))
            self.assertEqual(response.status_code, 404, name)
        response = self.client.post(reverse("logs:delete", args=[self.log.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(LearningLog.objects.filter(pk=self.log.pk).exists())

    def test_list_only_shows_own_logs(self):
        self.client.login(username="bob", password="S3cure-pass!")
        response = self.client.get(reverse("logs:list"))
        self.assertNotContains(response, "Decorators")

    def test_create_log_with_tags(self):
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.post(
            reverse("logs:create"),
            {
                "title": "Generators",
                "topic": self.topic.pk,
                "date": timezone.localdate().isoformat(),
                "description": "Lazy evaluation",
                "tags_text": "Python, python,  Memory ",
            },
        )
        self.assertEqual(response.status_code, 302)
        log = LearningLog.objects.get(title="Generators")
        self.assertEqual(log.user, self.alice)
        self.assertEqual(sorted(t.name for t in log.tags.all()), ["memory", "python"])

    def test_cannot_use_another_users_topic(self):
        self.client.login(username="bob", password="S3cure-pass!")
        response = self.client.post(
            reverse("logs:create"),
            {
                "title": "Sneaky",
                "topic": self.topic.pk,
                "date": timezone.localdate().isoformat(),
                "description": "x",
            },
        )
        self.assertEqual(response.status_code, 200)  # form re-rendered with errors
        self.assertFalse(LearningLog.objects.filter(title="Sneaky").exists())

    def test_future_date_rejected(self):
        self.client.login(username="alice", password="S3cure-pass!")
        future = timezone.localdate() + timezone.timedelta(days=3)
        response = self.client.post(
            reverse("logs:create"),
            {"title": "Future", "topic": self.topic.pk, "date": future.isoformat(), "description": "x"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(LearningLog.objects.filter(title="Future").exists())

    def test_search_filters_results(self):
        LearningLog.objects.create(
            user=self.alice, title="Indexes", topic=self.topic, description="SQL"
        )
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.get(reverse("logs:list"), {"q": "Indexes"})
        self.assertContains(response, "Indexes")
        self.assertNotContains(response, "Decorators")

    def test_topic_with_logs_cannot_be_deleted(self):
        self.client.login(username="alice", password="S3cure-pass!")
        self.client.post(reverse("logs:topic_delete", args=[self.topic.pk]))
        self.assertTrue(Topic.objects.filter(pk=self.topic.pk).exists())

    def test_unused_tags_are_cleaned_up(self):
        tag = Tag.objects.create(user=self.alice, name="old")
        self.log.tags.add(tag)
        self.client.login(username="alice", password="S3cure-pass!")
        self.client.post(
            reverse("logs:edit", args=[self.log.pk]),
            {
                "title": "Decorators",
                "topic": self.topic.pk,
                "date": timezone.localdate().isoformat(),
                "description": "Notes",
                "tags_text": "new",
            },
        )
        self.assertFalse(Tag.objects.filter(name="old").exists())
        self.assertTrue(Tag.objects.filter(name="new").exists())
