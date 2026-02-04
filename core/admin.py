from django.contrib import admin
from .models import UserProfile, Space, CreditTransaction, ExchangeRequest
from .models import ExchangeMessage  # add

@admin.register(ExchangeMessage)
class ExchangeMessageAdmin(admin.ModelAdmin):
    list_display = ("request", "sender", "created_at")
    search_fields = ("sender__username", "text")

@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "space", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("requester__username", "space__title")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "credits")
    search_fields = ("user__username", "location")


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "location", "created_at")
    search_fields = ("title", "owner__username", "location")


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "reason", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "reason")
