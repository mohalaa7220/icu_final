from django.db import models
from users.models import Doctor, Nurse, Patient
import cloudinary.uploader
from django.contrib.postgres.fields import ArrayField


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
        ordering = ('-created',)

    def __str__(self):
        return self.name


class PatientMedicalImage(models.Model):
    name = models.CharField(max_length=220, null=True, blank=True)
    images = ArrayField(models.TextField(), blank=True, null=True)
    url = models.URLField(blank=True, max_length=200000)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='patient_medical_image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.patient.name

    def save(self, *args, **kwargs):
        if self.images:
            urls = []
            for image_data in self.images:
                response = cloudinary.uploader.upload(image_data)
                urls.append(response['url'])
            self.url = urls
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class PatientRaysImage(models.Model):
    name = models.CharField(max_length=220, null=True, blank=True)
    images = ArrayField(models.TextField(), blank=True, null=True)
    url = models.URLField(blank=True, max_length=200000)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='patient_rays_image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.patient.name

    def save(self, *args, **kwargs):
        if self.images:
            urls = []
            for image_data in self.images:
                response = cloudinary.uploader.upload(image_data)
                urls.append(response['url'])
            self.url = urls
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class Image(models.Model):
    image = models.ImageField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Image {self.id}"

    def save(self, *args, **kwargs):
        if self.image:
            response = cloudinary.uploader.upload(self.image)
            self.url = response['url']
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
