from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from books.models import Book
from logs.models import LearningLog, Tag, Topic

User = get_user_model()

TOPICS = {
    "Python": "Language features, libraries and idioms.",
    "Django": "Web framework notes: ORM, views, templates.",
    "Databases": "SQL, indexing and data modelling.",
    "Web Design": "HTML, CSS, Bootstrap and accessibility.",
}

LOGS = [
    ("List comprehensions vs. generator expressions", "Python", ["python", "performance"],
     "Generators are lazy and use constant memory. Use a list comprehension when you need the "
     "whole list; use a generator expression when you only iterate once."),
    ("Context managers and the with statement", "Python", ["python", "patterns"],
     "Any object with __enter__ and __exit__ works. contextlib.contextmanager turns a generator "
     "function into a context manager."),
    ("Django ORM: select_related vs prefetch_related", "Django", ["django", "orm", "performance"],
     "select_related uses a SQL JOIN for ForeignKey/OneToOne. prefetch_related runs a second "
     "query and joins in Python, which is needed for ManyToMany."),
    ("Class-based vs function-based views", "Django", ["django", "views"],
     "Function-based views are explicit and easy to read. Class-based views give reuse through "
     "mixins but hide control flow."),
    ("Protecting views with login_required", "Django", ["django", "security"],
     "Always filter querysets by request.user and use get_object_or_404 so other users' objects "
     "return 404."),
    ("Database indexes", "Databases", ["sql", "performance"],
     "An index speeds up reads on the indexed columns but slows down writes. Index columns used "
     "in WHERE, JOIN and ORDER BY."),
    ("Normalisation basics", "Databases", ["sql", "design"],
     "Store each fact once. Split repeated groups into separate tables linked with foreign keys."),
    ("Bootstrap grid and breakpoints", "Web Design", ["css", "bootstrap", "responsive"],
     "Columns are 12-wide. Use col-12 col-md-6 col-xl-3 to stack on phones and spread out on "
     "larger screens."),
    ("Accessible forms", "Web Design", ["accessibility", "html"],
     "Every input needs a label. Show errors in text next to the field, not only with colour."),
    ("Environment variables for configuration", "Django", ["django", "deployment"],
     "Keep secrets such as SECRET_KEY and DATABASE_URL out of source control and read them from "
     "the environment."),
]

BOOKS = [
    ("Fluent Python", "Luciano Ramalho", "Technology", Book.Status.READING, None,
     "Chapters on data model and decorators are excellent."),
    ("Two Scoops of Django", "Daniel Feldroy", "Technology", Book.Status.COMPLETED, 5,
     "Practical best practices for real Django projects."),
    ("Designing Data-Intensive Applications", "Martin Kleppmann", "Technology",
     Book.Status.TO_READ, None, "Recommended for understanding databases at scale."),
    ("Atomic Habits", "James Clear", "Self-help", Book.Status.COMPLETED, 4,
     "Small habits compound. The habit-stacking idea is useful for daily study."),
    ("Deep Work", "Cal Newport", "Self-help", Book.Status.READING, None,
     "Schedule distraction-free blocks for learning."),
    ("Sapiens", "Yuval Noah Harari", "History", Book.Status.TO_READ, None, ""),
    ("The Pragmatic Programmer", "Andrew Hunt, David Thomas", "Technology",
     Book.Status.COMPLETED, 5, "Timeless advice on craft and tooling."),
]


class Command(BaseCommand):
    help = "Create a demo user with sample topics, learning logs and books."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="demo")
        parser.add_argument("--password", default="demo12345")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the demo user's existing data before creating new entries.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com"}
        )
        if created:
            user.set_password(options["password"])
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}'."))
        else:
            self.stdout.write(f"User '{username}' already exists.")

        if options["reset"]:
            LearningLog.objects.filter(user=user).delete()
            Book.objects.filter(user=user).delete()
            Tag.objects.filter(user=user).delete()
            Topic.objects.filter(user=user).delete()
            self.stdout.write("Existing data removed.")
        elif LearningLog.objects.filter(user=user).exists() or Book.objects.filter(user=user).exists():
            self.stdout.write(
                self.style.WARNING("User already has data. Use --reset to recreate demo entries.")
            )
            return

        topics = {
            name: Topic.objects.get_or_create(user=user, name=name, defaults={"description": desc})[0]
            for name, desc in TOPICS.items()
        }

        today = timezone.localdate()
        for index, (title, topic_name, tag_names, description) in enumerate(LOGS):
            log = LearningLog.objects.create(
                user=user,
                title=title,
                topic=topics[topic_name],
                description=description,
                date=today - timedelta(days=index * 2),
            )
            tags = [Tag.objects.get_or_create(user=user, name=n)[0] for n in tag_names]
            log.tags.set(tags)

        for title, author, category, status, rating, notes in BOOKS:
            Book.objects.create(
                user=user, title=title, author=author, category=category,
                status=status, rating=rating, notes=notes,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data ready: {len(LOGS)} logs, {len(BOOKS)} books.\n"
                f"Log in with username '{username}' and password '{options['password']}'."
            )
        )
