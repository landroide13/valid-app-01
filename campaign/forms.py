from django import forms

from account.models import Profile, UserRole
from .models import Campaign, CampaignEngagement

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
        ]
        widgets = {
            "problem_summary": forms.Textarea(attrs={"rows": 5}),
            "solution_summary": forms.Textarea(attrs={"rows": 5}),
            "pilot_offer_summary": forms.Textarea(attrs={"rows": 4}),
        }


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











