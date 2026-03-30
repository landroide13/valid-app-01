from django.db import models
from django.conf import settings

class UserRole(models.TextChoices):
    FOUNDER = "founder", "Founder"
    SME = "sme", "SME"
    ADMIN = "admin", "Admin"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=UserRole.choices)
    company_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    pain_points = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"    






