
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    path("reports/", views.reports, name="reports"),
    

    path("<str:module>/", views.record_list, name="record_list"),

    path(
        "<str:module>/add/",
        views.record_create,
        name="record_create"
    ),

    path(
        "<str:module>/edit/<int:pk>/",
        views.record_edit,
        name="record_edit"
    ),

    path(
        "<str:module>/delete/<int:pk>/",
        views.record_delete,
        name="record_delete"
    ),
       
]
