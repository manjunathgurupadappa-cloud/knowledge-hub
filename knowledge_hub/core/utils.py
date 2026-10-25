from django.core.paginator import Paginator


def paginate(request, queryset, per_page=10):
    """Return (page_obj, querystring) where querystring keeps the active filters."""
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return page_obj, params.urlencode()
