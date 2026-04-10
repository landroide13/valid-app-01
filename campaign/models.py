from django.db import models
from django.conf import settings


class UserRole(models.TextChoices):
    FOUNDER = "founder", "Founder"
    SME = "sme", "SME"
    ADMIN = "admin", "Admin"

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

class CampaignIndustry(models.TextChoices):
    LOGISTICS = "logistics", "Logistics"
    TRANSPORT = "transport", "Transport"
    CONSTRUCTION = "construction", "Construction"
    FIELD_SERVICE = "field_service", "Field Service"
    MANUFACTURING = "manufacturing", "Manufacturing"
    FINANCE = "finance", "Finance"
    HR = "hr", "HR"
    OTHER = "other", "Other"

class CampaignTargetRole(models.TextChoices):
    OPERATIONS_MANAGER = "operations_manager", "Operations Manager"
    FLEET_MANAGER = "fleet_manager", "Fleet Manager"
    FINANCE_MANAGER = "finance_manager", "Finance Manager"
    CEO = "ceo", "CEO / Founder"
    IT_MANAGER = "it_manager", "IT Manager"
    HR_MANAGER = "hr_manager", "HR Manager"
    OTHER = "other", "Other"

class CampaignCompanySize(models.TextChoices):
    SIZE_1_10 = "1_10", "1–10 employees"
    SIZE_10_25 = "10_25", "10–25 employees"
    SIZE_25_100 = "25_100", "25–100 employees"
    SIZE_100_250 = "100_250", "100–250 employees"
    SIZE_250_PLUS = "250_plus", "250+ employees"

class CampaignValidationGoal(models.TextChoices):
    DISCOVERY_CALLS = "discovery_calls", "Discovery Calls"
    PILOT_DISCUSSIONS = "pilot_discussions", "Pilot Discussions"
    LETTERS_OF_INTENT = "letters_of_intent", "Letters of Intent"
    DEPOSITS = "deposits", "Deposits"
    WAITLIST_SIGNUPS = "waitlist_signups", "Waitlist Signups"


class Campaign(models.Model):
    founder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns",
    )
    title = models.CharField(max_length=255)
    problem_summary = models.TextField()
    solution_summary = models.TextField()

    target_industry = models.CharField(
        max_length=50,
        choices=CampaignIndustry.choices,
    )
    target_role = models.CharField(
        max_length=50,
        choices=CampaignTargetRole.choices,
    )
    target_company_size = models.CharField(
        max_length=50,
        choices=CampaignCompanySize.choices,
    )
    target_market = models.CharField(max_length=100, blank=True)

    validation_goal_type = models.CharField(
        max_length=50,
        choices=CampaignValidationGoal.choices,
    )
    validation_goal_count = models.PositiveIntegerField(default=1)

    pilot_offer_summary = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=CampaignStatus.choices,
        default=CampaignStatus.PENDING_REVIEW,
    )

    campaign_image = models.ImageField(upload_to="campaign_visuals/", blank=True, null=True)
    #product_demo_url = models.URLField(blank=True)

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














