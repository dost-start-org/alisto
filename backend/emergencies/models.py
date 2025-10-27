from django.db import models
import uuid
from django.conf import settings
from django.db.models import Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class EmergencyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    icon_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EmergencyReport(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('Unverified', 'Unverified'),
        ('Verified', 'Verified'),
        ('Low confidence', 'Low confidence'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Responded', 'Responded'),
        ('Responding', 'Responding'),
        ('Resolved', 'Resolved'),
        ('Dismissed', 'Dismissed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    details = models.TextField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='Unverified'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    image_url = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports',
        help_text="The responder assigned to this emergency report."
    )

    def __str__(self):
        return f"Emergency Report {self.id}"

    def update_verification_status(self):
        """
        Updates the verification status of the report based on the votes in EmergencyVerification.
        """
        yes_votes = self.emergencyverification_set.filter(vote=True).count()
        no_votes = self.emergencyverification_set.filter(vote=False).count()

        if yes_votes > 0:
            self.verification_status = 'Verified'
        elif no_votes > 0:
            self.verification_status = 'Low confidence'
        else:
            self.verification_status = 'Unverified'

        self.save()

class EmergencyVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(EmergencyReport, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.BooleanField(null=True)
    details = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.report.id} by {self.user.email}"

    def save(self, *args, **kwargs):
        """
        Override the save method to update the verification status of the related EmergencyReport.
        """
        super().save(*args, **kwargs)
        self.report.update_verification_status()

class UserEvaluation(models.Model):
    STARS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    APP_GUIDE_CHOICES = [
        ('Yes', 'Yes'),
        ('Somewhat', 'Somewhat'),
        ('No', 'No')
    ]
    COMPLETION_SPEED_CHOICES = [
        ('Very fast', 'Very fast'),
        ('Acceptable', 'Acceptable'),
        ('Too slow', 'Too slow')
    ]
    CONFIDENCE_LEVEL_CHOICES = [
        ('Not confident', 'Not confident'),
        ('Neutral', 'Neutral'),
        ('Very confident', 'Very confident')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(EmergencyReport, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    stars = models.IntegerField(choices=STARS_CHOICES)
    did_app_guide_clearly = models.CharField(max_length=20, choices=APP_GUIDE_CHOICES)
    completion_speed = models.CharField(max_length=20, choices=COMPLETION_SPEED_CHOICES)
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVEL_CHOICES)
    improvement_suggestion = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation for {self.report.id}"

@receiver(post_save, sender=EmergencyReport)
def notify_report_status_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Notify reporter about the new report creation
        send_mail(
            subject='Emergency Report Submitted',
            message=f'Your report {instance.id} has been submitted successfully.',
            from_email='noreply@alisto.com',
            recipient_list=[instance.user.email]
        )
    else:
        # Notify reporter about status changes
        send_mail(
            subject='Emergency Report Status Update',
            message=f'The status of your report {instance.id} has been updated to {instance.status}.',
            from_email='noreply@alisto.com',
            recipient_list=[instance.user.email]
        )