from django.db import models
from users.models import Doctor, Nurse, Patient
# Create your models here.


class MedicalTest(models.Model):
    name = models.CharField(max_length=200)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, related_name='doctor_medical')
    nurse = models.ManyToManyField(Nurse, related_name='nurse_medical')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, related_name='patient_medical')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Medical Test'
        verbose_name_plural = 'Medical Test'

    def __str__(self):
        return self.name
