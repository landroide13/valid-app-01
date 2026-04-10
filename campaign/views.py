from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from .forms import CampaignEngagementForm, CampaignForm, ProfileForm, SignUpForm
from .models import (
    Campaign,
    CampaignCompanySize,
    CampaignIndustry,
    CampaignStatus,
    CampaignTargetRole,
    CampaignValidationGoal,
    IntroRequest,
    IntroRequestStatus,
)

def is_founder(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "founder"
    )


def is_sme(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "sme"
    )


def home(request):
    campaigns = (
        Campaign.objects.filter(status=CampaignStatus.LIVE)
        .select_related("founder", "founder__profile")
        .annotate(intro_requests_count=Count("intro_requests"))[:6]
    )

    return render(
        request,
        "campaign/home.html",
        {"campaigns": campaigns},
    )


def campaign_list(request):
    campaigns = (
        Campaign.objects.filter(status=CampaignStatus.LIVE)
        .select_related("founder", "founder__profile")
        .annotate(intro_requests_count=Count("intro_requests"))
    )

    industry = request.GET.get("industry")
    role = request.GET.get("role")
    company_size = request.GET.get("company_size")
    goal_type = request.GET.get("goal_type")
    market = request.GET.get("market")

    if industry:
        campaigns = campaigns.filter(target_industry=industry)
    if role:
        campaigns = campaigns.filter(target_role=role)
    if company_size:
        campaigns = campaigns.filter(target_company_size=company_size)
    if goal_type:
        campaigns = campaigns.filter(validation_goal_type=goal_type)
    if market:
        campaigns = campaigns.filter(target_market__icontains=market)

    return render( 
        request,
        "campaign/campaign_list.html",
        {   
            "campaigns": campaigns,
            "industry_choices": CampaignIndustry.choices,
            "role_choices": CampaignTargetRole.choices,
            "company_size_choices": CampaignCompanySize.choices,
            "goal_type_choices": CampaignValidationGoal.choices,
        },
    )


def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(
        Campaign.objects.select_related("founder", "founder__profile"),
        id=campaign_id,
        status=CampaignStatus.LIVE,
    )

    existing_intro_request = None
    can_request_intro = request.user.is_authenticated and is_sme(request.user)

    if can_request_intro:
        existing_intro_request = IntroRequest.objects.filter(
            campaign=campaign,
            sme_user=request.user,
        ).first()

    context = {
        "campaign": campaign,
        "can_request_intro": can_request_intro,
        "existing_intro_request": existing_intro_request,
    }
    return render(request, "campaign/campaign_detail.html", context)


@login_required
def founder_dashboard(request):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    campaigns = Campaign.objects.filter(founder=request.user).annotate(
        intro_requests_count=Count("intro_requests")
    )

    context = {
        "total_campaigns": campaigns.count(),
        "live_campaigns": campaigns.filter(status=CampaignStatus.LIVE).count(),
        "pending_campaigns": campaigns.filter(
            status=CampaignStatus.PENDING_REVIEW
        ).count(),
        "total_intro_requests": IntroRequest.objects.filter(
            campaign__founder=request.user
        ).count(),
        "recent_campaigns": campaigns[:5],
    }
    return render(request, "campaign/founder/dashboard.html", context)


@login_required
def founder_campaign_list(request):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    campaigns = Campaign.objects.filter(founder=request.user).annotate(
        intro_requests_count=Count("intro_requests")
    )

    return render(
        request,
        "campaign/founder/campaign_list.html",
        {"campaigns": campaigns},
    )


@login_required
def founder_campaign_create(request):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.founder = request.user
            campaign.status = CampaignStatus.PENDING_REVIEW
            campaign.save()
            messages.success(request, "Campaign submitted for review.")
            return redirect("founder_campaign_list")
    else:
        form = CampaignForm()

    return render(
        request,
        "campaign/founder/campaign_form.html",
        {
            "form": form,
            "page_title": "Create Campaign",
        },
    )


@login_required
def founder_campaign_update(request, campaign_id):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    campaign = get_object_or_404(Campaign, id=campaign_id, founder=request.user)

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            updated_campaign = form.save(commit=False)
            if updated_campaign.status in [
                CampaignStatus.REJECTED,
                CampaignStatus.LIVE,
                CampaignStatus.COMPLETED,
            ]:
                updated_campaign.status = CampaignStatus.PENDING_REVIEW
            updated_campaign.save()
            messages.success(request, "Campaign updated successfully.")
            return redirect("founder_campaign_list")
    else:
        form = CampaignForm(instance=campaign)

    return render(
        request,
        "campaign/founder/campaign_form.html",
        {
            "form": form,
            "campaign": campaign,
            "page_title": "Edit Campaign",
        },
    )


@login_required
def founder_intro_request_list(request):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    intro_requests = (
        IntroRequest.objects.filter(campaign__founder=request.user)
        .select_related("campaign", "sme_user", "sme_user__profile")
        .order_by("-requested_at")
    )

    return render(
        request,
        "campaign/founder/intro_request_list.html",
        {"intro_requests": intro_requests},
    )


@login_required
def founder_intro_request_update(request, intro_request_id, new_status):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    intro_request = get_object_or_404(
        IntroRequest,
        id=intro_request_id,
        campaign__founder=request.user,
    )

    if new_status not in [
        IntroRequestStatus.ACCEPTED,
        IntroRequestStatus.REJECTED,
    ]:
        messages.error(request, "Invalid intro request status.")
        return redirect("founder_intro_request_list")

    intro_request.status = new_status
    intro_request.save()

    if new_status == IntroRequestStatus.ACCEPTED:
        CampaignEngagement.objects.get_or_create(intro_request=intro_request)

    messages.success(request, f"Intro request marked as {new_status}.")
    return redirect("founder_intro_request_list")


@login_required
def founder_engagement_update(request, intro_request_id):
    if not is_founder(request.user):
        return HttpResponseForbidden("Only founders can access this page.")

    intro_request = get_object_or_404(
        IntroRequest,
        id=intro_request_id,
        campaign__founder=request.user,
        status=IntroRequestStatus.ACCEPTED,
    )

    engagement, _ = CampaignEngagement.objects.get_or_create(
        intro_request=intro_request
    )

    if request.method == "POST":
        form = CampaignEngagementForm(request.POST, instance=engagement)
        if form.is_valid():
            form.save()
            messages.success(request, "Engagement updated successfully.")
            return redirect("founder_intro_request_list")
    else:
        form = CampaignEngagementForm(instance=engagement)

    return render(
        request,
        "campaign/founder/engagement_form.html",
        {
            "form": form,
            "intro_request": intro_request,
        },
    )


@login_required
def sme_dashboard(request):
    if not is_sme(request.user):
        return HttpResponseForbidden("Only SMEs can access this page.")

    my_intro_requests = (
        IntroRequest.objects.filter(sme_user=request.user)
        .select_related("campaign", "campaign__founder")
        .order_by("-requested_at")
    )

    recommended_campaigns = (
        Campaign.objects.filter(status=CampaignStatus.LIVE)
        .exclude(intro_requests__sme_user=request.user)
        .select_related("founder", "founder__profile")[:5]
    )

    return render(
        request,
        "campaign/sme/dashboard.html",
        {
            "my_intro_requests": my_intro_requests,
            "recommended_campaigns": recommended_campaigns,
        },
    )


@login_required
def sme_request_intro(request, campaign_id):
    if not is_sme(request.user):
        return HttpResponseForbidden("Only SMEs can request intros.")

    campaign = get_object_or_404(
        Campaign,
        id=campaign_id,
        status=CampaignStatus.LIVE,
    )

    if campaign.founder == request.user:
        messages.error(request, "You cannot request an intro for your own campaign.")
        return redirect("campaign_detail", campaign_id=campaign.id)

    existing_request = IntroRequest.objects.filter(
        campaign=campaign,
        sme_user=request.user,
    ).first()

    if existing_request:
        messages.warning(request, "You already requested an intro for this campaign.")
        return redirect("campaign_detail", campaign_id=campaign.id)

    IntroRequest.objects.create(
        campaign=campaign,
        sme_user=request.user,
        status=IntroRequestStatus.REQUESTED,
    )

    messages.success(request, "Intro request sent successfully.")
    return redirect("sme_dashboard")


def signup_view(request):
    if request.user.is_authenticated:
        if is_founder(request.user):
            return redirect("founder_dashboard")
        elif is_sme(request.user):
            return redirect("sme_dashboard")
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Your account has been created successfully.")

            if user.profile.role == "founder":
                return redirect("founder_dashboard")
            return redirect("sme_dashboard")
    else:
        form = SignUpForm()

    return render(request, "campaign/auth/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if is_founder(request.user):
            return redirect("founder_dashboard")
        elif is_sme(request.user):
            return redirect("sme_dashboard")
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back.")

            if hasattr(user, "profile") and user.profile.role == "founder":
                return redirect("founder_dashboard")
            elif hasattr(user, "profile") and user.profile.role == "sme":
                return redirect("sme_dashboard")
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "campaign/auth/login.html", {"form": form})


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

            if profile.role == "founder":
                return redirect("founder_dashboard")
            return redirect("sme_dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "campaign/auth/profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )









