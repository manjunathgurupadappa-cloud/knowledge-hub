from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "rating", "user")
    list_filter = ("status", "category", "user")
    search_fields = ("title", "author")
