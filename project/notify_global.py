import logging

from firebase_admin import messaging
from fcm_django.models import FCMDevice
from notification.models import NotificationApp

from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone


logger = logging.getLogger(__name__)


def has_active_session(user):
    """
    Check if the user has an active session.
    """
    try:
        session_key = user.session_key
        print(f"session_key: {session_key}")  # Debug statement
        session = Session.objects.get(pk=session_key)
        last_activity = session.get_decoded().get('_last_activity')
        print(f"last_activity: {last_activity}")  # Debug statement
        if last_activity is not None:
            elapsed_time = timezone.now() - last_activity
            print(f"elapsed_time: {elapsed_time}")  # Debug statement
            if elapsed_time.total_seconds() >= settings.SESSION_COOKIE_AGE:
                # Session has expired
                raise Session.DoesNotExist
    except (Session.DoesNotExist, AttributeError):
        # User does not have an active session
        print('User does not have an active session')
        return

    return True


def send_notification(patient, user, device_token, title=''):
    """
    Send a notification to the user's registered devices.
    """
    if not has_active_session(user):
        logger.warning('User does not have an active session')
        return

    # Get the registered FCMDevice tokens
    devices = FCMDevice.objects.filter(
        user=user, registration_id=device_token, active=True)
    registration_ids = [device.registration_id for device in devices]

    # Send the notification to the registered devices
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

            logger.info(f'Message sent to device {i}')
        else:
            device = devices[i]
            device.is_active = False
            device.save()
            logger.error(
                f'Error sending message to device {i}: {result.exception}')
