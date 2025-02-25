from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    signup, user_login, user_logout,
    get_groups, messages, events,
    group_operations, EventViewSet,
    dashboard_data, notes
)

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"), 
    path("logout/", user_logout, name="logout"),
    path("groups/list/", get_groups, name="get_groups"),
    path("groups/", group_operations, name="group_operations"),
    path("messages/", messages, name="messages"),
    path("events/", events, name="events"),
    path("dashboard/", dashboard_data, name="dashboard_data"),
    path("notes/", notes, name="notes"),
    path('', include(router.urls)),
]
