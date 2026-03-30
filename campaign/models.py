from django.db import models
from django.conf import settings


class CampaignStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING_REVIEW = "pending_review", "Pending Review"
    LIVE = "live", "Live"
    COMPLETED = "completed", "Completed"
    REJECTED = "rejected", "Rejected"


class IntroRequestStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class EngagementOutcome(models.TextChoices):
    PILOT_DISCUSSION = "pilot_discussion", "Pilot Discussion"
    LETTER_OF_INTENT = "letter_of_intent", "Letter of Intent"
    DEPOSIT_RECEIVED = "deposit_received", "Deposit Received"
    FOLLOW_UP = "follow_up", "Follow Up"
    NOT_A_FIT = "not_a_fit", "Not a Fit"
    NO_DECISION = "no_decision", "No Decision"


class Campaign(models.Model):
    founder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns",
    )
    title = models.CharField(max_length=255)
    problem_summary = models.TextField()
    solution_summary = models.TextField()
    target_industry = models.CharField(max_length=100)
    target_role = models.CharField(max_length=100)
    target_company_size = models.CharField(max_length=50)
    target_market = models.CharField(max_length=100, blank=True)
    validation_goal_type = models.CharField(max_length=50)
    validation_goal_count = models.PositiveIntegerField(default=1)
    pilot_offer_summary = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=CampaignStatus.choices,
        default=CampaignStatus.PENDING_REVIEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class IntroRequest(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="intro_requests",
    )
    sme_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="intro_requests",
    )
    status = models.CharField(
        max_length=20,
        choices=IntroRequestStatus.choices,
        default=IntroRequestStatus.REQUESTED,
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("campaign", "sme_user")
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.sme_user.username} -> {self.campaign.title}"


class CampaignEngagement(models.Model):
    intro_request = models.OneToOneField(
        IntroRequest,
        on_delete=models.CASCADE,
        related_name="engagement",
    )
    discovery_call_scheduled = models.BooleanField(default=False)
    discovery_call_completed = models.BooleanField(default=False)
    outcome = models.CharField(
        max_length=30,
        choices=EngagementOutcome.choices,
        blank=True,
    )
    founder_notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Engagement for request {self.intro_request_id}"














