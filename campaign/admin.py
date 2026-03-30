from django.contrib import admin
from .models import Campaign, IntroRequest, CampaignEngagement

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "founder",
        "target_industry",
        "target_role",
        "status",
        "created_at",
    )
    list_filter = ("status", "target_industry", "target_role", "target_company_size")
    search_fields = ("title", "founder__username", "founder__email")


@admin.register(IntroRequest)
class IntroRequestAdmin(admin.ModelAdmin):
    list_display = ("campaign", "sme_user", "status", "requested_at")
    list_filter = ("status",)
    search_fields = ("campaign__title", "sme_user__username", "sme_user__email")


@admin.register(CampaignEngagement)
class CampaignEngagementAdmin(admin.ModelAdmin):
    list_display = (
        "intro_request",
        "discovery_call_scheduled",
        "discovery_call_completed",
        "outcome",
        "updated_at",
    )
    list_filter = ("discovery_call_scheduled", "discovery_call_completed", "outcome")







