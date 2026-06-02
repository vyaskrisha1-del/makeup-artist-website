from django.db import models
import uuid
from django.core.mail import send_mail
from django.conf import settings


# ----------------------------
# Service Model
# ----------------------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Enter duration in minutes")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ----------------------------
# Booking Model
# ----------------------------
class Booking(models.Model):

    SLOT_CHOICES = [
            ('09:00 AM', '09:00 AM'),
    ('09:30 AM', '09:30 AM'),
    ('10:00 AM', '10:00 AM'),
    ('10:30 AM', '10:30 AM'),
    ('11:00 AM', '11:00 AM'),
    ('11:30 AM', '11:30 AM'),
    ('12:00 PM', '12:00 PM'),
    ('12:30 PM', '12:30 PM'),
    ('01:00 PM', '01:00 PM'),
    ('01:30 PM', '01:30 PM'),
    ('02:00 PM', '02:00 PM'),
    ('02:30 PM', '02:30 PM'),
    ('03:00 PM', '03:00 PM'),
    ('03:30 PM', '03:30 PM'),
    ('04:00 PM', '04:00 PM'),
    ('04:30 PM', '04:30 PM'),
    ('05:00 PM', '05:00 PM'),
    ('05:30 PM', '05:30 PM'),
    ('06:00 PM', '06:00 PM'),
    ('06:30 PM', '06:30 PM'),
    ('07:00 PM', '07:00 PM'),
    ('07:30 PM', '07:30 PM'),
    ]

    LOCATION_CHOICES = [
        ('Studio Visit', 'Studio Visit'),
        ('Home Service', 'Home Service'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()

    slot = models.CharField(
        max_length=20,
        
    )

    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES
    )

    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------
    # Save Method
    # ----------------------------
    def save(self, *args, **kwargs):
        old_status = None

        if self.pk:
            old_status = Booking.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # Send cancellation email
        if old_status != "cancelled" and self.status == "cancelled" and self.email:
            send_mail(
                "Appointment Cancellation Notice",
                f"""
Hello {self.customer_name},

We are sorry, the makeup artist is not available on your selected slot.

Service: {self.service.name}
Date: {self.appointment_date}
Time: {self.slot}

Please choose another date or contact us.

Sorry for the inconvenience.
""",
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False
            )

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} - {self.appointment_date}"