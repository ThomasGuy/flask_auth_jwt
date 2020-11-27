import logging
import json

from flask_socketio import SocketIO, emit
from flask import request


log = logging.getLogger(__name__)
sockio = SocketIO( cors_allowed_origins=[])


@sockio.on('connect')
def test_connected():
    emit('my response', {'data': 'Connected'})
    log.info(f"socketio: {request.sid} connected")


@sockio.on('disconnect')
def test_disconnect():
    print(f"socketio: {request.sid} disconnected")
    log.info(f"socketio: {request.sid} disconnected")


@sockio.on('message', namespace='/api/ticker')
def messsage_handler(msg):
    emit('my response', {'data': msg['data']})


# @sockio.on('ticker_update')
# def handle_ticker_update(json):
#     emit('ticker_update', json)


@sockio.on('event')
def handle_event(json):
    emit('Ahoy there', {'data': 42})
