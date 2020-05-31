from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import json
from server.botmgr.query import QueryHandler

QueryHandler.instance()

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    if (isinstance(message, str)):
        message = json.loads(message)
    
    name = session.get('name')
    if name is None:
        name = message['name']

    room = session.get('room')
    if room is not None:
        emit('message', {'msg': name + ':' + message['msg'], 'sender': name}, room=room)
    else:
        emit('message', {'msg': name + ':' + message['msg'], 'sender': name})

    QueryHandler.instance().handle_query(message['msg'])

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

