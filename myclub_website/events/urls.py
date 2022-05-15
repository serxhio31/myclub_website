from django.urls import path

from . import views

# app_name = "events"

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path("events/", views.event_list, name="event_list"),
    path("events/<int:pk>/", views.event_details, name="event_details"),
]