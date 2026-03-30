from django import forms
from .models import Campaign, CampaignEngagement

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











