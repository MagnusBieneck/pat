"""Module where the models are registered for admin panel."""
from django.contrib import admin
from refund.models import Project, CostCentre, Refund

admin.site.register(Project)
admin.site.register(CostCentre)
admin.site.register(Refund)
