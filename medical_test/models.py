from django.db import models
from users.models import Doctor, Nurse, Patient
# Create your models here.

# lets us explicitly set upload path and filename


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


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


class PatientMedicalImage(models.Model):
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='patient_medical_image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.patient.name


class PatientRaysImage(models.Model):
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='patient_rays_image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.patient.name
