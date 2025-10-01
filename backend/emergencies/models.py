from django.db import models
import uuid
from accounts.models import UserProfile
from responders.models import ResponderUnit

class EmergencyReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Fire', 'Fire Emergency'),
        ('Crime', 'Crime Emergency'),
        ('Disaster', 'Disaster Emergency'),
        ('Ambulance', 'Ambulance/Medical Emergency'),
        ('Domestic Violence', 'Domestic Violence'),
        ('Medical Crisis', 'Medical Crisis'),
        ('Flood', 'Flood'),
        ('Other', 'Other Emergency'),
    ]
    REPORT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In-Progress', 'In-Progress Aiding'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    report_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the emergency report."
    )
    reported_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_reports',
        help_text="The user who reported the emergency (can be null for anonymous guests)."
    )
    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPE_CHOICES,
        help_text="Type of emergency being reported."
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude of the emergency location."
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude of the emergency location."
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed textual description of the emergency."
    )
    voice_report_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to an audio file of the voice-assisted report."
    )
    status = models.CharField(
        max_length=20,
        choices=REPORT_STATUS_CHOICES,
        default='Pending',
        help_text="Current status of the emergency report."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the report was submitted."
    )
    assigned_to_responder_unit = models.ForeignKey(
        ResponderUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports',
        help_text="The responder unit assigned to this emergency."
    )
    resolved_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_emergencies',
        help_text="The user (responder/LGU) who marked the emergency as resolved."
    )
    resolution_notes = models.TextField(
        blank=True,
        help_text="Notes on how the emergency was resolved."
    )

    def __str__(self):
        return f"Report {self.report_id} - {self.report_type} ({self.status})"

class VerificationRequest(models.Model):
    def get_verification_status(self):
        total = self.responses.count()
        if total == 0:
            return 'Unverified', 0
        yes_count = self.responses.filter(response='Yes').count()
        no_count = self.responses.filter(response='No').count()
        yes_ratio = yes_count / total
        if yes_ratio >= 0.7 and yes_count >= 3:
            return 'Verified', yes_ratio
        elif no_count / total >= 0.7 and no_count >= 3:
            return 'Flagged as False', yes_ratio
        else:
            return 'Unverified', yes_ratio
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Expired', 'Expired'),
    ]
    emergency_report = models.ForeignKey(
        EmergencyReport,
        on_delete=models.CASCADE,
        related_name='verification_requests',
        help_text="The emergency report this verification request is for."
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    targeted_users = models.ManyToManyField(
        'accounts.UserProfile',
        related_name='verification_requests',
        help_text="Users who received this verification request."
    )

    def __str__(self):
        return f"VerificationRequest for {self.emergency_report} at {self.requested_at}"

class VerificationResponse(models.Model):
    RESPONSE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    verification_request = models.ForeignKey(
        VerificationRequest,
        on_delete=models.CASCADE,
        related_name='responses',
        help_text="The verification request this response is for."
    )
    user = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='verification_responses',
        help_text="The user who responded."
    )
    response = models.CharField(max_length=3, choices=RESPONSE_CHOICES)
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('verification_request', 'user')

    def __str__(self):
        return f"{self.user} responded {self.response} to {self.verification_request}"

class ReportMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
    ]
    report = models.ForeignKey(
        EmergencyReport,
        on_delete=models.CASCADE,
        related_name='media',
        help_text="The emergency report this media belongs to."
    )
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        help_text="Type of media (image, video, or audio)."
    )
    file = models.FileField(
        upload_to='emergency_media/',
        help_text="The media file (image, video, or audio)."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the media was uploaded."
    )

    def __str__(self):
        return f"{self.media_type} for Report {self.report.report_id}"

class ResponseTimeLog(models.Model):
    report = models.OneToOneField(
        EmergencyReport,
        on_delete=models.CASCADE,
        related_name='response_time_log',
        help_text="The emergency report associated with this log."
    )
    dispatch_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the responder unit was dispatched."
    )
    arrival_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the responder unit arrived at the scene."
    )
    resolution_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the emergency was marked as resolved."
    )

    def __str__(self):
        return f"Response Log for Report {self.report.report_id}"