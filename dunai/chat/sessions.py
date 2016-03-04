import random


def session_init(request):
    if not request.session.get('chat_data'):
        request.session['chat_data'] = dict(
            id=random.getrandbits(64),
            username='Anonymous'
        )
    return request.session['chat_data']


# def session_get(request):
#     return request.session.get('chat_data')


def session_set(request, chat_data):
    request.session['chat_data'] = chat_data
