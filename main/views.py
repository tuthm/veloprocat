
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import BikeUnit, Booking, Category


def index(request):
    popular = (
        BikeUnit.objects
        .select_related("category")
        .order_by("pk")[:8]
    )

    return render(request, "index.html", {
        "units_count": BikeUnit.objects.count(),
        "popular": popular,
        "categories": Category.objects.all(),
    })


def catalog(request):
    units = BikeUnit.objects.select_related("category").all()

    category_slug = request.GET.get("category")
    query = request.GET.get("q", "").strip()

    if category_slug:
        units = units.filter(category__slug=category_slug)

    if query:
        units = units.filter(name__icontains=query)

    page_size = 20
    paginator_page = request.GET.get("page", 1)

    try:
        page = int(paginator_page)
    except (TypeError, ValueError):
        page = 1

    page = max(page, 1)

    total = units.count()
    pages = max(1, (total + page_size - 1) // page_size)
    page = min(page, pages)

    items = units[
        (page - 1) * page_size:page * page_size
    ]

    return render(request, "catalog.html", {
        "units": items,
        "total": total,
        "page": page,
        "pages": pages,
        "categories": Category.objects.all(),
        "active_category": category_slug or "",
        "query": query,
    })


def api_units(request):
    """JSON для живого поиска: /api/units/?q=merida"""

    query = request.GET.get("q", "").strip()

    units = BikeUnit.objects.select_related("category").all()

    if query:
        units = units.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )

    data = [
        {
            "id": unit.pk,
            "name": unit.name,
            "category": unit.category.name,
            "price": int(unit.price_per_day),
            "status": unit.status,
            "status_label": unit.get_status_display(),
        }
        for unit in units[:50]
    ]

    return JsonResponse({
        "count": len(data),
        "units": data,
    })


def unit_detail(request, pk):
    unit = get_object_or_404(
        BikeUnit.objects.select_related("category"),
        pk=pk
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("main:login")

        # BUG-07: велосипед определяется по URL страницы.
        # Скрытое поле формы не может подменить его ID.
        post_data = request.POST.copy()
        post_data["unit"] = str(unit.pk)

        form = BookingForm(post_data)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.user = request.user
            booking.unit = unit

            days = (
                booking.end_date - booking.start_date
            ).days

            booking.total = (
                unit.price_per_day * days
            )

            booking.status = Booking.STATUS_NEW
            booking.save()

            unit.status = BikeUnit.STATUS_RENTED
            unit.save(update_fields=["status"])

            return redirect("main:profile")

    else:
        form = BookingForm(
            initial={"unit": unit.pk}
        )

    return render(request, "unit_detail.html", {
        "unit": unit,
        "form": form,
    })


def prices(request):
    return render(request, "prices.html", {
        "categories": Category.objects.all()
    })


def about(request):
    return render(request, "about.html")


def contacts(request):
    return render(request, "contacts.html")


@login_required
def profile(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("unit")
        .order_by("-created_at")
    )

    return render(request, "profile.html", {
        "bookings": bookings
    })


class VeloprokatLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(
    request,
    user,
    backend="django.contrib.auth.backends.ModelBackend"
)

            return redirect("main:profile")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {
        "form": form
    })
