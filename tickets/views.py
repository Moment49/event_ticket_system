from django.shortcuts import render, redirect
from tickets.models import Ticket, Payment
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


CustomUser = get_user_model()


@login_required
def payment_process(request, pk):
    event = Event.objects.get(pk=pk)
    price = event.price
    user = CustomUser.objects.get(email=request.user)

    ticket_user = Ticket.objects.filter(user__email=request.user)
    for ticket in ticket_user:
        if event == ticket.event:
            print("User have registered for the event already")
            messages.error(request, "Sorry you have registered for the event already")
            return redirect('event_detail', pk=event.id)
        else:
            payment = Payment.objects.create(
                amount=price, status='Pending', event=event, user=user
            )
            # Simulating Payment Processing by changing status...
            payment.status = 'Completed'

            if payment.status == 'Completed':
                payment.save()
                # Generate the ticket 
                ticket = Ticket.objects.create(payment=payment, event=event, user=user)
                ticket.save()
                messages.success(request, 'Payment sucessful.. You can view your ticket Information')
                return redirect('user_dashboard_view')
            
            else:
                messages.error(request, 'Sorry Something went wrong. cannot process payment!!!')

    return redirect('event_detail', pk=event.id)
    
@login_required
def payment_success(request):
    return render(request, 'tickets/payment_success.html')

@login_required
def purchased_tickets(request):
    return render(request, 'tickets/purchased_tickets.html')