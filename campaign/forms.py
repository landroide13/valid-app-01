from django import forms
from account.models import Profile, UserRole
from .models import Campaign, CampaignEngagement, CampaignInvite
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    role = forms.ChoiceField(
        choices=[
            (UserRole.FOUNDER, "Founder"),
            (UserRole.SME, "SME"),
        ],
        required=True,
    )
    company_name = forms.CharField(max_length=255, required=False)
    industry = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    company_size = forms.CharField(max_length=50, required=False)
    job_title = forms.CharField(max_length=100, required=False)
    pain_points = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "role",
            "company_name",
            "industry",
            "country",
            "company_size",
            "job_title",
            "pain_points",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "role":
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs["placeholder"] = "Choose a username"
        self.fields["first_name"].widget.attrs["placeholder"] = "Your first name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Your last name"
        self.fields["email"].widget.attrs["placeholder"] = "you@company.com"
        self.fields["password1"].widget.attrs["placeholder"] = "Create a password"
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat your password"
        self.fields["company_name"].widget.attrs["placeholder"] = "Company or project name"
        self.fields["industry"].widget.attrs["placeholder"] = "Example: Logistics"
        self.fields["country"].widget.attrs["placeholder"] = "Example: France"
        self.fields["company_size"].widget.attrs["placeholder"] = "Example: 10–50"
        self.fields["job_title"].widget.attrs["placeholder"] = "Example: Founder or Operations Manager"
        self.fields["pain_points"].widget.attrs["placeholder"] = "Optional: describe your pain points or validation interests"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()

            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "role": self.cleaned_data["role"],
                    "company_name": self.cleaned_data["company_name"],
                    "industry": self.cleaned_data["industry"],
                    "country": self.cleaned_data["country"],
                    "company_size": self.cleaned_data["company_size"],
                    "job_title": self.cleaned_data["job_title"],
                    "pain_points": self.cleaned_data["pain_points"],
                },
            )

            if not created:
                profile.role = self.cleaned_data["role"]
                profile.company_name = self.cleaned_data["company_name"]
                profile.industry = self.cleaned_data["industry"]
                profile.country = self.cleaned_data["country"]
                profile.company_size = self.cleaned_data["company_size"]
                profile.job_title = self.cleaned_data["job_title"]
                profile.pain_points = self.cleaned_data["pain_points"]
                profile.save()

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "company_name",
            "industry",
            "country",
            "company_size",
            "job_title",
            "pain_points",
        ]
        widgets = {
            "pain_points": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            "title",
            "problem_summary",
            "solution_summary",
            "target_industry",
            "target_role",
            "target_company_size",
            "target_market",
            "validation_goal_type",
            "validation_goal_count",
            "pilot_offer_summary",
            "campaign_image",
        ]
        widgets = {
            "problem_summary": forms.Textarea(attrs={"rows": 5}),
            "solution_summary": forms.Textarea(attrs={"rows": 5}),
            "pilot_offer_summary": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "validation_goal_type": "Validation goal",
            "validation_goal_count": "Target number",
            "pilot_offer_summary": "Early adopter / pilot offer",
            "campaign_image": "Campaign visual",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["accept"] = "image/*"
            else:
                field.widget.attrs["class"] = "form-control"

        self.fields["title"].widget.attrs["placeholder"] = "Example: Route planning for regional transport SMEs"
        self.fields["problem_summary"].widget.attrs["placeholder"] = "Describe the operational problem you are validating."
        self.fields["solution_summary"].widget.attrs["placeholder"] = "Explain your proposed solution clearly."
        self.fields["target_market"].widget.attrs["placeholder"] = "Example: France, Germany, Europe"
        self.fields["validation_goal_count"].widget.attrs["placeholder"] = "Example: 5"
        self.fields["pilot_offer_summary"].widget.attrs["placeholder"] = "Describe what early adopters receive."    


class CampaignEngagementForm(forms.ModelForm):
    class Meta:
        model = CampaignEngagement
        fields = [
            "discovery_call_scheduled",
            "discovery_call_completed",
            "outcome",
            "founder_notes",
        ]
        widgets = {
            "founder_notes": forms.Textarea(attrs={"rows": 5}),
        }


class CampaignInviteForm(forms.ModelForm):
    class Meta:
        model = CampaignInvite
        fields = [
            "recipient_name",
            "recipient_email",
            "personal_message",
        ]
        widgets = {
            "personal_message": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "recipient_name": "Contact name",
            "recipient_email": "Contact email",
            "personal_message": "Personal message",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["recipient_name"].widget.attrs["placeholder"] = "Optional contact name"
        self.fields["recipient_email"].widget.attrs["placeholder"] = "contact@company.com"
        self.fields["personal_message"].widget.attrs["placeholder"] = (
            "Optional short message to explain why you are inviting this person."
        )








