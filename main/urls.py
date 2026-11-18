from django.urls import path

from . import views
app_name = "main"


urlpatterns = [
    path("", views.index, name="index"),
    path("catalog/", views.catalog, name="catalog"),
    path("api/units/", views.api_units, name="api_units"),
    path("unit/<int:pk>/", views.unit_detail, name="unit_detail"),
    path("prices/", views.prices, name="prices"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("profile/", views.profile, name="profile"),
   path("login/", views.VeloprokatLoginView.as_view(), name="login"),

    path("register/", views.register, name="register"),
]
