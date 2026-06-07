from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime, timedelta, date
from django.db import transaction
from django.contrib import messages

from .forms import BookingForm
from .models import Booking


# ----------------------------
# HOME
# ----------------------------
def home(request):
    return render(request, "core/index.html")


# ----------------------------
# SERVICES
# ----------------------------
def birdal_makeup(request):
    return render(request, "core/services/birdal_makeup.html")


def glam_makeup(request):
    return render(request, "core/services/glam_makeup.html")


def hair_styling(request):
    return render(request, "core/services/hair_styling.html")


def skincare(request):
    return render(request, "core/services/skincare.html")


def waxing(request):
    return render(request, "core/services/waxing.html")


def pre_wedding(request):
    return render(request, "core/services/pre_wedding.html")


# ----------------------------
# AVAILABLE SLOTS (SAFE VERSION)
# ----------------------------
def get_available_slots(request):

    selected_date = request.GET.get('date')

    if not selected_date:
        return JsonResponse({'slots': []})

    all_slots = [
        '09:00 AM','09:30 AM','10:00 AM','10:30 AM',
        '11:00 AM','11:30 AM','12:00 PM','12:30 PM',
        '01:00 PM','01:30 PM','02:00 PM','02:30 PM',
        '03:00 PM','03:30 PM','04:00 PM','04:30 PM',
        '05:00 PM','05:30 PM','06:00 PM','06:30 PM',
        '07:00 PM','07:30 PM',
    ]

    try:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except:
        return JsonResponse({'slots': []})

    booked_slots = Booking.objects.filter(
        appointment_date=selected_date_obj
    ).values_list('slot', flat=True)

    available_slots = [
        slot for slot in all_slots
        if slot not in booked_slots
    ]

    return JsonResponse({'slots': available_slots})


# ----------------------------
# BOOKING VIEW (SAFE VERSION)
# ----------------------------
def booking_view(request):

    form = BookingForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            booking = form.save(commit=False)

            if not booking.slot or not booking.service:
                messages.error(request, "Please select service and slot")
                return render(request, "core/booking.html", {"form": form})

            with transaction.atomic():

                conflict = Booking.objects.filter(
                    appointment_date=booking.appointment_date,
                    slot=booking.slot
                ).exists()

                if conflict:
                    messages.error(request, "Slot already booked")
                    return render(request, "core/booking.html", {"form": form})

                booking.save()

            messages.success(request, "Booking successful!")
            return redirect("booking_success")

        else:
            messages.error(request, "Form invalid")

    return render(request, "core/booking.html", {"form": form})


# ----------------------------
# SUCCESS PAGE
# ----------------------------
def booking_success(request):
    return render(request, "core/booking_success.html")


# ----------------------------
# TEST EMAIL
# ----------------------------
def test_email(request):

    send_mail(
        "Test Email",
        "Email working",
        settings.EMAIL_HOST_USER,
        ["bbcare1402@gmail.com"],
        fail_silently=False
    )

    return HttpResponse("Email sent")

def test_email(request):
    from django.core.mail import send_mail

    send_mail(
        "Test Email",
        "This is working",
        settings.EMAIL_HOST_USER,
        ["bbcare1402@gmail.com"],
        fail_silently=False
    )

    return HttpResponse("Email Sent")