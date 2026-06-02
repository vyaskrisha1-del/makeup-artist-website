from django.contrib import admin, messages
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import quote

from .models import Booking, Service


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'service',
        'appointment_date',
        'slot',
        'colored_status',
        'phone',
        'whatsapp_button'
    )

    actions = ['mark_confirmed', 'mark_cancelled']

    # -------------------
    # Colored Status
    # -------------------
    def colored_status(self, obj):
        if obj.status == "pending":
            color = "orange"
            label = "🟡 Pending"
        elif obj.status == "confirmed":
            color = "green"
            label = "🟢 Confirmed"
        else:
            color = "red"
            label = "🔴 Cancelled"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            label
        )

    colored_status.short_description = "Status"

    # -------------------
    # WhatsApp Button
    # -------------------
    def whatsapp_button(self, obj):

        # Confirmed booking WhatsApp
        if obj.status == "confirmed":
            message = (
                f"Hello {obj.customer_name}\n\n"
                f"Your booking has been confirmed.\n\n"
                f"Service: {obj.service.name}\n"
                f"Date: {obj.appointment_date}\n"
                f"Time: {obj.slot}\n"
                f"Location: {obj.location_type}\n\n"
                f"Thank you for booking with us ✨"
            )

        # Cancelled booking WhatsApp ONLY if email not provided
        elif obj.status == "cancelled" and not obj.email:
            message = (
                f"Hello {obj.customer_name}\n\n"
                f"We are sorry, the makeup artist is not available on your preferred slot.\n\n"
                f"Service: {obj.service.name}\n"
                f"Date: {obj.appointment_date}\n"
                f"Time: {obj.slot}\n\n"
                f"Please contact us to book another slot."
            )

        else:
            return "Pending"

        encoded_message = quote(message, safe='')
        phone = obj.phone.replace("+", "").replace(" ", "")

        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

        return format_html(
            '<a href="{}" target="_blank" '
            'style="background:#25D366;color:white;padding:6px 12px;'
            'border-radius:6px;text-decoration:none;">Send WhatsApp</a>',
            whatsapp_url
        )

    whatsapp_button.short_description = "WhatsApp"

    # -------------------
    # Confirm Booking Action
    # -------------------
    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):

        for booking in queryset:
            booking.status = "confirmed"
            booking.save()

            # Send confirmation email if email exists
            if booking.email:
                send_mail(
                    "Appointment Confirmed",
                    f"""
Hello {booking.customer_name},

Great news! Your appointment has been confirmed.

Service: {booking.service.name}
Date: {booking.appointment_date}
Time: {booking.slot}

We look forward to seeing you.
""",
                    settings.EMAIL_HOST_USER,
                    [booking.email],
                    fail_silently=False
                )

        self.message_user(
            request,
            "Selected bookings confirmed and emails sent.",
            messages.SUCCESS
        )

    # -------------------
    # Cancel Booking Action
    # -------------------
    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):

        for booking in queryset:
            booking.status = "cancelled"
            booking.save()

            # Send cancellation email ONLY if email exists
            if booking.email:
                send_mail(
                    "Appointment Cancellation Notice",
                    f"""
Hello {booking.customer_name},

We are sorry to inform you that the makeup artist is not available on your preferred slot.

Service: {booking.service.name}
Date: {booking.appointment_date}
Time: {booking.slot}

Please choose another date or contact us for rescheduling.

Sorry for the inconvenience.
""",
                    settings.EMAIL_HOST_USER,
                    [booking.email],
                    fail_silently=False
                )

        self.message_user(
            request,
            "Selected bookings cancelled. Email sent where available.",
            messages.SUCCESS
        )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active')