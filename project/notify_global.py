import logging
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from notification.models import NotificationApp
from users.models import User

logger = logging.getLogger(__name__)


def send_notification(patient, user, device_token, title='', user_sender=''):
    headnursing_users = User.objects.filter(role='headnursing')

    device_headnursing_users = FCMDevice.objects.filter(
        user__in=headnursing_users)

    devices = FCMDevice.objects.filter(
        registration_id=device_token, active=True)

    user_devices = devices.filter(user=user)

    if not user_devices.exists():
        logger.warning('User is not associated with device token')
        return

    registration_tokens = []

    # Loop through the devices associated with head nursing colleagues
    for device in device_headnursing_users:
        registration_tokens.append(device.registration_id)

    # Loop through the devices associated with the user
    for device in user_devices:
        registration_tokens.append(device.registration_id)

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title, body=f"{title} for Patient ({patient.name}) in room number {patient.room_number}"),
        tokens=registration_tokens,
    )

    users = [device.user for device in devices]

    response = messaging.send_multicast(message)
    for i, result in enumerate(response.responses):
        if result.success:
            for user in users:
                if user.role != 'headnursing':
                    NotificationApp.objects.create(
                        patient=patient,
                        title=title,
                        message=f"{title} for Patient ({patient.name}) in room number {patient.room_number}",
                        user_receiver=user,
                        user_sender=user_sender
                    )
            print(f'Message sent to device {i}')
        else:
            device = devices[i]
            device.is_active = False
            device.save()
            logger.error(
                f'Error sending message to device {i}: {result.exception}')
