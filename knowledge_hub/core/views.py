from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from books.models import Book
from logs.models import LearningLog, Topic


@login_required
def dashboard(request):
    user = request.user
    logs = LearningLog.objects.filter(user=user)
    books = Book.objects.filter(user=user)

    total_books = books.count()
    status_counts = {
        row["status"]: row["n"] for row in books.values("status").annotate(n=Count("id"))
    }
    progress = []
    for value, label in Book.Status.choices:
        count = status_counts.get(value, 0)
        percent = round(count * 100 / total_books) if total_books else 0
        progress.append({"key": value, "label": label, "count": count, "percent": percent})

    week_start = timezone.localdate() - timedelta(days=6)

    context = {
        "total_logs": logs.count(),
        "total_books": total_books,
        "total_topics": Topic.objects.filter(user=user).count(),
        "logs_this_week": logs.filter(date__gte=week_start).count(),
        "progress": progress,
        "recent_logs": logs.select_related("topic")[:5],
        "recent_books": books.order_by("-created_at")[:5],
        "topic_stats": Topic.objects.filter(user=user)
        .annotate(log_count=Count("logs"))
        .order_by("-log_count", "name")[:6],
    }
    return render(request, "core/dashboard.html", context)
