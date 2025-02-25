from django.urls import path
from .views import signup, user_login, user_logout, get_groups, messages, events, group_operations


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("groups/list/", get_groups, name="get_groups"),
    path("groups/", group_operations, name="group_operations"),
    path("messages/", messages, name="messages"),
    path("events/", events, name="events"),
]
