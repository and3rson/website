from django.http import JsonResponse
from django.shortcuts import render
import json
from . import sessions
from . import helpers
from dunai.chat.management.commands.chatlistener import CLIENT_INBOX, ADMIN_INBOX


def view(request):
    chat_data = sessions.session_init(request)
    return render(request, 'dunai/chat.jade', dict())


def set_name(request):
    chat_data = sessions.session_init(request)
    chat_data['username'] = request.GET.get('name') or 'Anonymous'
    sessions.session_set(request, chat_data)
    return JsonResponse(dict(result=True))


def poll(request):
    chat_data = sessions.session_init(request)
    message = helpers.expect(CLIENT_INBOX.format(chat_id=chat_data['id']))
    return JsonResponse(dict(result=message[1] if message else None))


def send(request):
    chat_data = sessions.session_init(request)
    helpers.publish(
        ADMIN_INBOX.format(chat_id=chat_data['id']),
        json.dumps(dict(chat_data=chat_data, message=request.GET.get('message')))
    )
    return JsonResponse(dict(result=True))
