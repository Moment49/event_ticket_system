from django.shortcuts import render, redirect
from tickets.models import Ticket, Payment
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

CustomUser = get_user_model()

# Create your views here.
def send_ticket_email(request, user, to_email, ticket_id, ticket_event, ticket_payment):
    subject = "Your Event Ticket"
    message = render_to_string(
        'tickets/ticket_sent.html',
        context={
            'user': user.first_name,
            'ticket_id': ticket_id,
            'ticket_event':ticket_event,
            'ticket_payment':ticket_payment
        }
    )
    email = EmailMessage(subject, message, to=[to_email])
    return email


@login_required
def payment_process(request, pk):
    event = Event.objects.get(pk=pk)
    price = event.price
    user = CustomUser.objects.get(email=request.user)
    
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
        email = send_ticket_email(request, user, user.email, ticket_id=ticket.id, ticket_event=ticket.event, ticket_payment=ticket.payment)
        email.send()
        return redirect('payment_sucesss')
    else:
        messages.error(request, 'Sorry Something went wrong. cannot process payment!!!')

    return redirect('event_detail', pk=event.id)
    
@login_required
def payment_success(request):
    return render(request, 'tickets/payment_success.html')