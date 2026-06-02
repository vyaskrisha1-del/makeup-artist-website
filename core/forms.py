from django import forms
from .models import Booking, Service
from datetime import date, datetime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'customer_name',
            'phone',
            'email',
            'service',
            'appointment_date',
            'slot',
            'location_type',
            'address',
            'notes'
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'placeholder': 'Enter your full name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'placeholder': 'Enter phone number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'required': False,
                'placeholder': 'Enter email address'
            }),

            'service': forms.Select(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100'
            }),

            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'appointment_date',
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-200',
                'min': date.today().strftime('%Y-%m-%d')
            }),

            'slot': forms.Select(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'id': 'slot-field'
            }),

            'location_type': forms.Select(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100'
            }),

            'address': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'placeholder': 'Enter address (only for home service)',
                'rows': 4
            }),

            'notes': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 rounded-2xl border border-pink-100',
                'placeholder': 'Special notes (optional)',
                'rows': 4
            }),
        }

    # ----------------------------
    # INIT
    # ----------------------------
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['email'].required = False
        self.fields['service'].empty_label = "Select Service"

        self.fields['service'].queryset = Service.objects.filter(
            is_active=True
        )

        selected_date = None

        if self.data.get('appointment_date'):
            selected_date = self.data.get('appointment_date')

        # ALL SLOTS
        all_slots = [
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

        available_slots = []

        booked_slots = []

        now = datetime.now()

        # GET BOOKED SLOTS
        if selected_date:

            booked_slots = Booking.objects.filter(
                appointment_date=selected_date
            ).values_list('slot', flat=True)

        for slot_value, slot_label in all_slots:

            slot_time = datetime.strptime(
                slot_value,
                "%I:%M %p"
            ).time()

            # REMOVE PAST SLOTS FOR TODAY
            if selected_date == str(date.today()):

                if slot_time <= now.time():
                    continue

            # REMOVE BOOKED SLOTS
            if slot_value in booked_slots:
                continue

            available_slots.append(
                (slot_value, slot_label)
            )

        self.fields['slot'].choices = available_slots
        if self.data.get('slot'):

         selected_slot = self.data.get('slot')

         if selected_slot not in [s[0] for s in available_slots]:

          available_slots.insert(
            0,
            (selected_slot, selected_slot)
        )

        self.fields['slot'].choices = available_slots
        for field_name in self.errors:

         css_class = self.fields[field_name].widget.attrs.get(
        'class',
        ''
    )

         self.fields[field_name].widget.attrs['class'] = (
         css_class +
         ' border-red-500 ring-1 ring-red-500'
    )
    

        self.fields['slot'].choices = available_slots
    # ----------------------------
    # NAME VALIDATION
    # ----------------------------
    def clean_customer_name(self):

        customer_name = self.cleaned_data.get(
        'customer_name',
        ''
         ).strip()

        if len(customer_name) < 3:
          raise forms.ValidationError(
            "Please enter at least 3 characters."
        )

        if any(char.isdigit() for char in customer_name):
          raise forms.ValidationError(
            "Numbers are not allowed in your name."
        )

        return customer_name

    # ----------------------------
    # PHONE VALIDATION
    # ----------------------------
    def clean_phone(self):

     phone = self.cleaned_data.get(
        'phone',
        ''
    ).strip()

     if not phone.isdigit():
        raise forms.ValidationError(
            "Phone number should contain digits only."
        )

     if len(phone) != 10:
        raise forms.ValidationError(
            "Phone number must be exactly 10 digits."
        )

     return phone

    # ----------------------------
    # ADDRESS VALIDATION
    # ----------------------------
    def clean_address(self):

     address = self.cleaned_data.get('address')
     location_type = self.cleaned_data.get('location_type')

     if (
        location_type == "Home Service"
        and not address
    ):
        raise forms.ValidationError(
            "Please enter your address for home service."
        )

     return address

    # ----------------------------
    # DATE VALIDATION
    # ----------------------------
    def clean_appointment_date(self):

        appointment_date = self.cleaned_data.get('appointment_date')

        if appointment_date < date.today():
            raise forms.ValidationError(
                "You cannot book a past date."
            )

        return appointment_date

    # ----------------------------
    # SLOT VALIDATION
    # ----------------------------
    def clean(self):

        cleaned_data = super().clean()

        appointment_date = cleaned_data.get('appointment_date')
        slot = cleaned_data.get('slot')

        if appointment_date and slot:

            existing_booking = Booking.objects.filter(
                appointment_date=appointment_date,
                slot=slot
            ).exists()

            if existing_booking:

                self.add_error(
                    'slot',
                    "This slot is already booked."
                )

        return cleaned_data