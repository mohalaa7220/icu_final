from django.db import models
from users.models import Doctor, Nurse, Patient
# Create your models here.


class Rays(models.Model):
    name = models.CharField(max_length=200)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, related_name='doctor_rays')
    nurse = models.ManyToManyField(Nurse, related_name='nurse_rays')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, related_name='patient_rays')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Rays'
        verbose_name_plural = 'Rays'

    def __str__(self):
        return self.name
