from django.urls import path
from . import views
from django.urls import path
from .views import booking_view, booking_success

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "services/birdal-makeup/",
        views.birdal_makeup,
        name="birdal_makeup",
    ),

    path(
        "services/glam-makeup/",
        views.glam_makeup,
        name="glam_makeup",
    ),

    path(
        "services/hair-styling/",
        views.hair_styling,
        name="hair_styling",
    ),

    path(
        "services/skincare/",
        views.skincare,
        name="skincare",
    ),

    path(
        "services/waxing/",
        views.waxing,
        name="waxing",
    ),

    path(
        "services/pre-wedding/",
        views.pre_wedding,
        name="pre_wedding",
    ),

    # Booking
    path('booking/',
          views.booking_view,
            name='booking'),


    path('booking-success/',
          views.booking_success,
            name='booking_success'),


    path('get-available-slots/',
          views.get_available_slots,
            name='get_available_slots'),
    
 

urlpatterns = [
    path('booking/', booking_view, name='booking'),
    path('booking-success/', booking_success, name='booking_success'),
]
            
]
