from django import forms

from core.forms import BootstrapFormMixin

from .models import Book


class BookForm(BootstrapFormMixin, forms.ModelForm):
    rating = forms.TypedChoiceField(
        required=False,
        choices=[("", "No rating")] + [(i, f"{i} / 5") for i in range(1, 6)],
        coerce=int,
        empty_value=None,
    )

    class Meta:
        model = Book
        fields = ["title", "author", "category", "status", "rating", "notes"]
        widgets = {
            "category": forms.TextInput(
                attrs={"list": "category-options", "placeholder": "Pick or type a category"}
            ),
            "notes": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = " ".join(self.cleaned_data["title"].split())
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title

    def clean_category(self):
        return " ".join(self.cleaned_data["category"].split()) or "Other"

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        rating = cleaned.get("rating")
        if status == Book.Status.TO_READ and rating:
            self.add_error("rating", "You can only rate a book after you start reading it.")
        return cleaned

    def save(self, commit=True):
        book = super().save(commit=False)
        book.user = self.user
        if commit:
            book.save()
        return book
