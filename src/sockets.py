from flask_socketio import SocketIO, emit
from app import socketio


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': message['data']})
#
#
# @socketio.on('my broadcast event')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)
#
#
# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})
#
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')
