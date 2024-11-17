# >>>>>> managesession.py >>>>>> 
from django.contrib.sessions.backends.db import SessionStore
def set_session_keys(keys, response):
    session = SessionStore()

    for key, value in keys.items():
        session[key] = value

    session.create()
    response.set_cookie('session_key', session.session_key)
    return response

def get_session_key(request):
    session_key = request.COOKIES.get('session_key')
    session = SessionStore(session_key=session_key)
    return session

def clear_all_session(request, response):
    request.session.flush()
    response.delete_cookie('session_key')
    return response
