from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.space_list, name="space_list"),
    path("spaces/<int:pk>/", views.space_detail, name="space_detail"),
    path("spaces/new/", views.space_create, name="space_create"),

    path("spaces/<int:space_id>/request/", views.send_exchange_request, name="send_exchange_request"),
    path("my-requests/", views.my_requests, name="my_requests"),
    path("requests/<int:pk>/accept/", views.accept_request, name="accept_request"),
    path("requests/<int:pk>/reject/", views.reject_request, name="reject_request"),
    path("requests/<int:pk>/chat/", views.request_chat, name="request_chat"),

    path("my-account/", views.my_account, name="my_account"),

    path("billing/", views.billing_page, name="billing"),
    path("billing/create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("billing/success/", views.billing_success, name="billing_success"),
    path("billing/cancel/", views.billing_cancel, name="billing_cancel"),

    # AUTH
    path("login/", auth_views.LoginView.as_view(
        template_name="core/login.html"
    ), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
]
