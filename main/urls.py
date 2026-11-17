from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog/", views.catalog, name="catalog"),
    path("unit/<int:pk>/", views.unit_detail, name="unit_detail"),
    path("prices/", views.prices, name="prices"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("account/", views.account, name="account"),
    path("search/", views.search, name="search"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
