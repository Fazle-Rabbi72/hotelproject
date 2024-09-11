from django.contrib import admin
from .models import Booking
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

class bookingAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','hotel_name', 'status', 'booking_date', 'check_in_date', 'check_out_date']

    def first_name(self, obj):
        return obj.users.users.first_name

    def last_name(self, obj):
        return obj.users.users.last_name

    def hotel_name(self, obj):
        return obj.hotel.title

    def save_model(self, request, obj, form, change):
        # Get the original booking status before saving
        original_status = Booking.objects.get(pk=obj.pk).status if obj.pk else None
        
        # Save the booking
        obj.save()

        # If the status is changed to "Completed" and balance hasn't been deducted
        if original_status != "Completed" and obj.status == "Completed":
            # Check if the user has enough balance
            if obj.users.balance >= obj.hotel.price:
                # Deduct the balance and save the user
                obj.users.balance -= obj.hotel.price
                obj.users.save()

                # Send email confirmation for booking completion
                email_subject = "Booking Completed"
                email_body = render_to_string('confirm_mail.html', {
                    'first_name': obj.users.users.first_name,
                    'last_name': obj.users.users.last_name,
                    'hotel_name': obj.hotel.title,
                    'booking_date': obj.booking_date.strftime('%Y-%m-%d'),
                    'check_in_date': obj.check_in_date.strftime('%Y-%m-%d') if obj.check_in_date else "N/A",
                    'check_out_date': obj.check_out_date.strftime('%Y-%m-%d') if obj.check_out_date else "N/A",
                })
                
                # Send the email
                email = EmailMultiAlternatives(email_subject, '', to=[obj.users.users.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            else:
                # If balance is insufficient, raise a validation error
                raise ValidationError("Insufficient balance to complete the booking.") 

admin.site.register(Booking, bookingAdmin)
