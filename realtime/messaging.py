from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict

from .events import *

channel_layer = get_channel_layer()


def send_event_request(event_request):
    _send_realtime_event_to_user(
        to_user_ids=[event_request.to_user.id],
        realtime_event=RequestEvent(
            id=event_request.id,
            event=event_request.event.id,
            from_user=event_request.from_user.id,
            to_user=event_request.to_user.id,
            decision=event_request.decision,
            created=event_request.created,
        )
    )


def send_event_response_request(event_request):
    _send_realtime_event_to_user(
        to_user_ids=[event_request.to_user.id],
        realtime_event=RequestEvent(
            id=event_request.id,
            event=event_request.event.id,
            from_user=event_request.to_user.id,
            to_user=event_request.from_user.id,
            decision=event_request.decision,
            created=event_request.created,
        )
    )


def send_message(message, members_ids):
    _send_realtime_event_to_user(
        to_user_ids=members_ids,
        realtime_event=MessageEvent(
            from_user=model_to_dict(message.from_user),
            text=message.text,
            created=message.created,
            event=message.event.id,
        )
    )


def send_private_message(message, members_ids):
    _send_realtime_event_to_user(
        to_user_ids=members_ids,
        realtime_event=PrivateMessageEvent(
            from_user=message.from_user.id,
            user=message.user.id,
            text=message.text,
            created=message.created,
        )
    )


def _send_realtime_event_to_user(to_user_ids, realtime_event):
    async_to_sync(channel_layer.send)(
        'realtime-event-sender',
        {
            'type': 'send_event',
            'to_user_ids': list(to_user_ids),
            'realtime_event_dict': realtime_event.properties_dict,
        }
    )
