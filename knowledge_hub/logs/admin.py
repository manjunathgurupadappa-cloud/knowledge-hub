from django.contrib import admin

from .models import LearningLog, Tag, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)


@admin.register(LearningLog)
class LearningLogAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "user", "date")
    list_filter = ("user", "topic")
    search_fields = ("title", "description")
