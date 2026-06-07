rom datetime import datetime, timedelta
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse

from .forms import BookingForm
from .models import Booking

def get_available_slots(request):

    selected_date = request.GET.get('date')
    print("SELECTED_DATE:",selected_date)

    all_slots = [
        '09:00 AM',
        '09:30 AM',
        '10:00 AM',
        '10:30 AM',
        '11:00 AM',
        '11:30 AM',
        '12:00 PM',
        '12:30 PM',
        '01:00 PM',
        '01:30 PM',
        '02:00 PM',
        '02:30 PM',
        '03:00 PM',
        '03:30 PM',
        '04:00 PM',
        '04:30 PM',
        '05:00 PM',
        '05:30 PM',
        '06:00 PM',
        '06:30 PM',
        '07:00 PM',
        '07:30 PM',
    ]

    available_slots = []

    try:

        selected_date_obj = datetime.strptime(
            selected_date,
            '%Y-%m-%d'
        ).date()
    except:
        try:
            selected_date_obj = datetime.strptime(selected_date,'%m/%d/%y').date()

        except:

         return JsonResponse({
            'slots': []
        })

    # GET BOOKED SLOTS

    booked_slots = Booking.objects.filter(
        appointment_date=selected_date_obj
    ).values_list('slot', flat=True)

    current_datetime = datetime.now()

    for slot in all_slots:

        slot_datetime = datetime.strptime(
            f"{selected_date} {slot}",
            "%Y-%m-%d %I:%M %p"
        )

        # REMOVE PAST SLOTS ONLY FOR TODAY

        if selected_date_obj == date.today():

            if slot_datetime <= current_datetime:
                continue

        # REMOVE BOOKED SLOTS

        if slot in booked_slots:
            continue

        available_slots.append(slot)
        print("BOOKED:", list(booked_slots))
        print("AVAILABLE:", available_slots)

    return JsonResponse({
        'slots': available_slots
    })
# ----------------------------
# Home & Service Views
# ----------------------------
def home(request):
    return render(request, "core/index.html")


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
# Generate blocked slots
# ----------------------------

def generate_slots(start_slot, duration):
    slots = []

    try:
        duration = int(duration)
        start_time = datetime.strptime(start_slot, "%I:%M %p")
    except Exception as e:
        print("Slot generation error:", e)
        return []

    total_slots = duration // 30
    if total_slots == 0:
        total_slots = 1

    for i in range(total_slots):
        slot_time = start_time + timedelta(minutes=i * 30)
        slots.append(slot_time.strftime("%I:%M %p"))

    return slots
# ----------------------------
# Booking View
# ----------------------------
def booking_view(request):

    form = BookingForm(request.POST or None)

    if request.method == "POST":

        print("=" * 40)
        print("BOOKING REQUEST RECEIVED")
        print(request.POST)
        print("=" * 40)

        if form.is_valid():

            try:
                booking = form.save(commit=False)

                print("FORM VALID")
                print("SLOT:", booking.slot)

                duration = booking.service.duration
                required_slots = generate_slots(booking.slot, duration)

                print("REQUIRED SLOTS:", required_slots)

                with transaction.atomic():

                    # check overlapping bookings
                    conflict = Booking.objects.filter(
                        appointment_date=booking.appointment_date,
                        slot__in=required_slots
                    ).exists()

                    if conflict:
                        messages.error(request, "Slot already booked.")
                        return render(request, "core/booking.html", {"form": form})

                    booking.save()
                    print("BOOKING SAVED:", booking.id)

                # -----------------------------
                # EMAILS (SAFE - WON'T BREAK FLOW)
                # -----------------------------

                try:
                    if booking.email:
                        send_mail(
                            "Booking Received",
                            f"""
Hi {booking.customer_name},

Your booking is received.

Service: {booking.service.name}
Date: {booking.appointment_date}
Slot: {booking.slot}

We will confirm soon.
""",
                            settings.EMAIL_HOST_USER,
                            [booking.email],
                            fail_silently=True
                        )
                except Exception as e:
                    print("Customer email failed:", e)

                try:
                    send_mail(
                        "New Booking",
                        f"""
Customer: {booking.customer_name}
Phone: {booking.phone}
Email: {booking.email}
Service: {booking.service.name}
Date: {booking.appointment_date}
Slot: {booking.slot}
""",
                        settings.EMAIL_HOST_USER,
                        ["bbcare1402@gmail.com"],
                        fail_silently=True
                    )
                except Exception as e:
                    print("Admin email failed:", e)

                return redirect("booking_success")

            except Exception as e:
                print("BOOKING ERROR:", e)
                messages.error(request, f"Error: {e}")

        else:
            print("FORM ERRORS:", form.errors)

    return render(request, "core/booking.html", {"form": form})


# ----------------------------
# Success View
# ----------------------------
def booking_success(request):
    return render(request, "core/booking_success.html")