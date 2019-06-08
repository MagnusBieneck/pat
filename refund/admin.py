"""Module where the models are registered for admin panel."""
from django.contrib import admin
from refund.models import Refund

admin.site.register(Refund)
