import logging

from flask import request
from flask_socketio import SocketIO, emit

# import json


log = logging.getLogger(__name__)
sockio = SocketIO(cors_allowed_origins=[])


@sockio.on('connect')
def test_connected():
    emit('my response', {'data': 'Connected'})
    log.info(f'socketio: {request.sid} connected')  # type: ignore


@sockio.on('disconnect')
def test_disconnect():
    print(f'socketio: {request.sid} disconnected')  # type: ignore
    log.info(f'socketio: {request.sid} disconnected')  # type: ignore


@sockio.on('message', namespace='/api/ticker')
def messsage_handler(msg):
    emit('my response', {'data': msg['data']})


# @sockio.on('ticker_update')
# def handle_ticker_update(json):
#     emit('ticker_update', json)


@sockio.on('event')
def handle_event(payload):
    emit('Ahoy there checkout this event! ', {'data': 42})
