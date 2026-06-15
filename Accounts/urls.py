from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "users/",
        views.user_list,
        name="users"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

]