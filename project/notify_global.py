from firebase_admin import messaging, firestore
from fcm_django.models import FCMDevice
from django.utils import timezone

from notification.models import NotificationApp


def send_notification(patient, user, device_token, title=''):
    # Get the registered FCMDevice tokens
    devices = FCMDevice.objects.filter(user=user, registration_id=device_token)
    registration_ids = [device.registration_id for device in devices]

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title, body=f"{title} for Patient ({patient.name}) in room number {patient.room_number}"),
        tokens=registration_ids,
    )

    response = messaging.send_multicast(message)
    for i, result in enumerate(response.responses):
        if result.success:
            NotificationApp.objects.create(
                patient=patient,
                title=title,
                message=f"{title} for Patient ({patient.name}) in room number {patient.room_number}",
            )

            print(f'Message sent to device {i}')
        else:
            device = devices[i]
            device.is_active = False
            device.save()
            print(
                f'Error sending message to device {i}: {result.exception}')
