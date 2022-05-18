from django.urls import path

from . import views

app_name = "pinax_messages"

urlpatterns = [
    path("inbox/", views.InboxView.as_view(),
        name="inbox"),
    path("create/", views.MessageCreateView.as_view(),
        name="message_create"),
    path("create/<int:user_id>/", views.MessageCreateView.as_view(),
        name="message_user_create"),
    path("thread/<int:pk>/", views.ThreadView.as_view(),
        name="thread_detail"),
    path("thread/<int:pk>/delete/", views.ThreadDeleteView.as_view(),
        name="thread_delete"),
]
