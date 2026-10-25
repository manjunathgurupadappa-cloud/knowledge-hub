from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Book

User = get_user_model()


class BookTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="S3cure-pass!")
        self.bob = User.objects.create_user("bob", password="S3cure-pass!")
        self.book = Book.objects.create(
            user=self.alice, title="Fluent Python", author="Luciano Ramalho",
            category="Technology", status=Book.Status.READING,
        )

    def test_login_required(self):
        response = self.client.get(reverse("books:list"))
        self.assertEqual(response.status_code, 302)

    def test_other_user_gets_404(self):
        self.client.login(username="bob", password="S3cure-pass!")
        for name in ("detail", "edit", "delete"):
            response = self.client.get(reverse(f"books:{name}", args=[self.book.pk]))
            self.assertEqual(response.status_code, 404, name)
        self.client.post(reverse("books:delete", args=[self.book.pk]))
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_create_book(self):
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.post(
            reverse("books:create"),
            {"title": "Deep Work", "author": "Cal Newport", "category": "Self-help",
             "status": "completed", "rating": "4", "notes": "Good"},
        )
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get(title="Deep Work")
        self.assertEqual((book.user, book.rating), (self.alice, 4))

    def test_cannot_rate_unread_book(self):
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.post(
            reverse("books:create"),
            {"title": "Unread", "author": "A", "category": "Other",
             "status": "to_read", "rating": "5", "notes": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Book.objects.filter(title="Unread").exists())

    def test_filter_by_status_and_search(self):
        Book.objects.create(user=self.alice, title="Sapiens", author="Harari",
                            category="History", status=Book.Status.TO_READ)
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.get(reverse("books:list"), {"status": "to_read"})
        self.assertContains(response, "Sapiens")
        self.assertNotContains(response, "Fluent Python")
        response = self.client.get(reverse("books:list"), {"q": "ramalho"})
        self.assertContains(response, "Fluent Python")


class DashboardAndAuthTests(TestCase):
    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)

    def test_register_logs_user_in(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newuser", "email": "new@example.com",
             "password1": "Str0ng-Passw0rd!", "password2": "Str0ng-Passw0rd!"},
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_logout_requires_post_and_redirects(self):
        User.objects.create_user("alice", password="S3cure-pass!")
        self.client.login(username="alice", password="S3cure-pass!")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
