from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, BikeUnit, Booking
from .forms import LoginForm, RegisterForm

def index(request):
    ctx = {
        "categories": Category.objects.all(),
        "popular": BikeUnit.objects.filter(is_popular=True)[:4],
    }
    return render(request, "index.html", ctx)

def catalog(request):
    units = BikeUnit.objects.select_related("category").order_by("id")
    cat = request.GET.get("category")
    if cat:
        units = units.filter(category__slug=cat)
    q = request.GET.get("q")
    if q:
        units = units.filter(name__icontains=q)
    paginator = Paginator(units, 20)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "catalog.html", {
        "page_obj": page, "categories": Category.objects.all(),
        "current_cat": cat, "q": q or "",
    })

def unit_detail(request, pk):
    unit = get_object_or_404(BikeUnit.objects.select_related("category"), pk=pk)
    same = BikeUnit.objects.filter(category=unit.category).exclude(pk=unit.pk)[:3]
    return render(request, "unit_detail.html", {"unit": unit, "same": same})

def prices(request):
    return render(request, "prices.html", {"categories": Category.objects.prefetch_related("units")})

def about(request):
    return render(request, "about.html")

def contacts(request):
    return render(request, "contacts.html")

@login_required
def account(request):
    bookings = Booking.objects.filter(user=request.user).select_related("unit").order_by("-created_at")
    return render(request, "account.html", {"bookings": bookings})

def search(request):
    q = request.GET.get("q", "").strip()
    units = BikeUnit.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)) if q else BikeUnit.objects.none()
    return render(request, "search.html", {"q": q, "units": units})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("main:index")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user:
            login(request, user)
            return redirect("main:account")
        form.add_error(None, "Неверный логин или пароль")
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("main:index")

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно. Добро пожаловать!")
        return redirect("main:index")
    return render(request, "register.html", {"form": form})
