from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.utils import paginate

from .forms import LearningLogForm, TopicForm
from .models import LearningLog, Tag, Topic


# ----------------------------------------------------------------- logs
@login_required
def log_list(request):
    logs = (
        LearningLog.objects.filter(user=request.user)
        .select_related("topic")
        .prefetch_related("tags")
    )
    q = request.GET.get("q", "").strip()
    topic_id = request.GET.get("topic", "").strip()
    tag = request.GET.get("tag", "").strip()

    if q:
        logs = logs.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(topic__name__icontains=q)
            | Q(tags__name__icontains=q)
        ).distinct()
    if topic_id.isdigit():
        logs = logs.filter(topic_id=int(topic_id))
    if tag:
        logs = logs.filter(tags__name=tag)

    page_obj, querystring = paginate(request, logs)
    context = {
        "page_obj": page_obj,
        "querystring": querystring,
        "q": q,
        "selected_topic": topic_id,
        "selected_tag": tag,
        "topics": Topic.objects.filter(user=request.user),
        "tags": Tag.objects.filter(user=request.user),
    }
    return render(request, "logs/log_list.html", context)


@login_required
def log_detail(request, pk):
    log = get_object_or_404(
        LearningLog.objects.select_related("topic").prefetch_related("tags"),
        pk=pk,
        user=request.user,
    )
    return render(request, "logs/log_detail.html", {"log": log})


@login_required
def log_create(request):
    form = LearningLogForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        log = form.save()
        messages.success(request, "Learning log added.")
        return redirect(log)
    context = {
        "form": form,
        "page_title": "New learning log",
        "submit_label": "Save log",
        "cancel_url": reverse("logs:list"),
    }
    if not Topic.objects.filter(user=request.user).exists():
        context.update(
            notice="You need at least one topic before you can add a log.",
            notice_url=reverse("logs:topic_list"),
            notice_label="Create a topic",
        )
    return render(request, "form_page.html", context)


@login_required
def log_edit(request, pk):
    log = get_object_or_404(LearningLog, pk=pk, user=request.user)
    form = LearningLogForm(request.POST or None, instance=log, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Learning log updated.")
        return redirect(log)
    return render(
        request,
        "form_page.html",
        {
            "form": form,
            "page_title": "Edit learning log",
            "submit_label": "Save changes",
            "cancel_url": log.get_absolute_url(),
        },
    )


@login_required
def log_delete(request, pk):
    log = get_object_or_404(LearningLog, pk=pk, user=request.user)
    if request.method == "POST":
        log.delete()
        Tag.objects.filter(user=request.user, logs__isnull=True).delete()
        messages.success(request, "Learning log deleted.")
        return redirect("logs:list")
    return render(
        request,
        "confirm_delete.html",
        {
            "page_title": "Delete learning log",
            "object_label": log.title,
            "cancel_url": log.get_absolute_url(),
        },
    )


# --------------------------------------------------------------- topics
@login_required
def topic_list(request):
    form = TopicForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Topic added.")
        return redirect("logs:topic_list")

    topics = Topic.objects.filter(user=request.user).annotate(log_count=Count("logs"))
    return render(request, "logs/topic_list.html", {"form": form, "topics": topics})


@login_required
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    form = TopicForm(request.POST or None, instance=topic, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Topic updated.")
        return redirect("logs:topic_list")
    return render(
        request,
        "form_page.html",
        {
            "form": form,
            "page_title": "Edit topic",
            "submit_label": "Save changes",
            "cancel_url": reverse("logs:topic_list"),
        },
    )


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk, user=request.user)
    log_count = topic.logs.count()
    if request.method == "POST":
        if log_count:
            messages.error(
                request, "This topic still has learning logs. Move or delete them first."
            )
        else:
            topic.delete()
            messages.success(request, "Topic deleted.")
        return redirect("logs:topic_list")
    return render(
        request,
        "confirm_delete.html",
        {
            "page_title": "Delete topic",
            "object_label": topic.name,
            "cancel_url": reverse("logs:topic_list"),
            "blocked": log_count > 0,
            "blocked_message": f"This topic has {log_count} learning log(s). "
            "Move or delete them before deleting the topic.",
        },
    )
