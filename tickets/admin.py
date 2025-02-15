from django.contrib import admin

from tickets.models import Ticket, Payment
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Payment)
