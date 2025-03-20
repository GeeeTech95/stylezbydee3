from django.db import models



class StaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(employment_status="terminated")

