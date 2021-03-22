from flask_socketio import emit, ConnectionRefusedError
from flask_login import current_user

from app import socketio


# Dummy callback function
def messageReceived(methods=['GET', 'POST']):
    # Callback get the same args as the parent function
    print('message was received!!!')


# Create a socket route listen for the message on the event
# "Chat message"
@socketio.on('Chat message')
def chat_handler(json, methods=['GET', 'POST']):
    # Here 'json' is contents of the message
    # Can also use flask_login and flask.request to get other
    # attributes
    # emit broadcasts a reply to the client(s)
    # This will be picked up by clients waiting for message on 'Chat Reply'
    # Here we simply return the original json
    # broadcast=True will send our message to everyone who is connected
    # broadcast=False will only send message to the current user
    # Callback call another function at emit, could be print/logging etc
    # Doesn't work when broadcast=True
    emit('Chat Reply', json, broadcast=True, callback=messageReceived)


# Connection route for new clients
# New clients connecting on Websocket will pass through this
@socketio.on('connect')
def connect_user():
    # Use flask login to check to see if user is allowed to connect
    if current_user.is_authenticated:
        # Print that the user is connected
        print(current_user, 'is connected')
        # emit a reply to the clients, this would be used to tiger an action
        # client side
        # We could also return a json object would would work with client
        # side callback function
        emit('Connection response', {'User Name': current_user.username,
                                     'Status': 'Connected'})
    # If the user isn't logged in, Raise an error.
    else:
        raise ConnectionRefusedError('unauthorized!')
