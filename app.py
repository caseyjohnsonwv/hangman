import env
from state_machine import *
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
)

@app.route('/sms', methods=['GET','POST'])
def sms_reply():
    # retrieve game state
    try:
        state = session['gameState']
    except KeyError:
        state = StateMachine.FIRST_TIME_LOAD
    # retrieve user's message and prepare response
    msg = request.form['Body']
    resp = MessagingResponse()

    # first time load
    if state == StateMachine.FIRST_TIME_LOAD:
        if 'new game' in msg.lower().strip():
            state = StateMachine.NEW_GAME
        else:
            resp.message("Hello! To play, text 'new game'!")

    # new game
    if state == StateMachine.NEW_GAME:
        resp.message("Starting a new game- text 'quit' at any time to stop.")

    # in progress
    if state == StateMachine.IN_PROGRESS:
        pass

    # game over
    if state == StateMachine.GAME_OVER:
        resp.message("Game over- text 'new game' to play again!")

    # state undefined
    if state == StateMachine.UNDEFINED:
        raise StateMachineError()

    # send response
    return str(resp)

if __name__ == '__main__':
    app.run()
