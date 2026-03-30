from django.urls import path
from .views import (
    campaign_detail,
    campaign_list,
    founder_campaign_create,
    founder_campaign_list,
    founder_campaign_update,
    founder_dashboard,
    founder_engagement_update,
    founder_intro_request_list,
    founder_intro_request_update,
    home,
    sme_dashboard,
    sme_request_intro,
)


urlpatterns = [
    path("", home, name="home"),
    path("campaigns/", campaign_list, name="campaign_list"),
    path("campaigns/<int:campaign_id>/", campaign_detail, name="campaign_detail"),

    path("founder/dashboard/", founder_dashboard, name="founder_dashboard"),
    path("founder/campaigns/", founder_campaign_list, name="founder_campaign_list"),
    path("founder/campaigns/create/", founder_campaign_create, name="founder_campaign_create"),
    path("founder/campaigns/<int:campaign_id>/edit/", founder_campaign_update, name="founder_campaign_update"),
    path("founder/intro-requests/", founder_intro_request_list, name="founder_intro_request_list"),
    path(
        "founder/intro-requests/<int:intro_request_id>/<str:new_status>/",
        founder_intro_request_update,
        name="founder_intro_request_update",
    ),
    path(
        "founder/intro-requests/<int:intro_request_id>/engagement/",
        founder_engagement_update,
        name="founder_engagement_update",
    ),

    path("sme/dashboard/", sme_dashboard, name="sme_dashboard"),
    path("campaigns/<int:campaign_id>/request-intro/", sme_request_intro, name="sme_request_intro"),
]











