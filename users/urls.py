from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.UserLogin.as_view(), name="user-login"),
    path(
        "create",
        views.UserCreation.as_view(),
        name="add-user",
    )
]

