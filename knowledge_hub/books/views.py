from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.utils import paginate

from .forms import BookForm
from .models import Book


def _form_context(form, title, submit_label, cancel_url):
    return {
        "form": form,
        "page_title": title,
        "submit_label": submit_label,
        "cancel_url": cancel_url,
        "datalist": Book.CATEGORY_SUGGESTIONS,
    }


@login_required
def book_list(request):
    own_books = Book.objects.filter(user=request.user)
    books = own_books

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()

    if q:
        books = books.filter(
            Q(title__icontains=q)
            | Q(author__icontains=q)
            | Q(category__icontains=q)
            | Q(notes__icontains=q)
        )
    if status in Book.Status.values:
        books = books.filter(status=status)
    else:
        status = ""
    if category:
        books = books.filter(category=category)

    counts = {row["status"]: row["n"] for row in own_books.values("status").annotate(n=Count("id"))}
    status_tabs = [{"value": "", "label": "All", "count": own_books.count()}] + [
        {"value": value, "label": label, "count": counts.get(value, 0)}
        for value, label in Book.Status.choices
    ]

    page_obj, querystring = paginate(request, books)
    context = {
        "page_obj": page_obj,
        "querystring": querystring,
        "q": q,
        "selected_status": status,
        "selected_category": category,
        "status_tabs": status_tabs,
        "categories": own_books.order_by("category").values_list("category", flat=True).distinct(),
    }
    return render(request, "books/book_list.html", context)


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    return render(request, "books/book_detail.html", {"book": book})


@login_required
def book_create(request):
    form = BookForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        book = form.save()
        messages.success(request, "Book added.")
        return redirect(book)
    return render(
        request, "form_page.html",
        _form_context(form, "Add a book", "Save book", reverse("books:list")),
    )


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    form = BookForm(request.POST or None, instance=book, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book updated.")
        return redirect(book)
    return render(
        request, "form_page.html",
        _form_context(form, "Edit book", "Save changes", book.get_absolute_url()),
    )


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("books:list")
    return render(
        request,
        "confirm_delete.html",
        {
            "page_title": "Delete book",
            "object_label": book.title,
            "cancel_url": book.get_absolute_url(),
        },
    )
