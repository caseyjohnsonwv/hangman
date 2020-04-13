import env
from hangman import *
from state_machine import *
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
)


def save_game(game):
    session['gameData'] = game.to_json()
def load_game():
    return HangmanGame.from_json(session['gameData'])


@app.route('/sms', methods=['POST'])
def sms_reply():
    # retrieve game state
    try:
        state = session['gameState']
    except KeyError:
        state = StateMachine.FIRST_TIME_LOAD

    # retrieve user's message and prepare response
    msg = request.form['Body'].upper().strip()
    resp = MessagingResponse()

    # first time load
    if state == StateMachine.FIRST_TIME_LOAD:
        if 'NEW GAME' in msg:
            state = StateMachine.NEW_GAME
        else:
            resp.message("Hello! Text 'new game' to play.")

    # new game
    if state == StateMachine.NEW_GAME:
        resp.message("Starting a new game. Text a letter to guess, or text 'later' at any time to stop.")
        g = HangmanGame("English")
        resp.message(g.blanks)
        save_game(g)
        state = StateMachine.IN_PROGRESS
    # in progress
    elif state == StateMachine.IN_PROGRESS:
        g = load_game()
        if 'LATER' in msg:
            state = StateMachine.LATER
        else:
            try:
                g.sanitize_guess(msg)
            except InvalidGuessError:
                resp.message("Whoops- I didn't understand your guess! Try again.")
            except LetterAlreadyGuessedError:
                resp.message("Whoops- you already guessed that letter! Try again.")
            else:
                if g.guess(msg):
                    state = StateMachine.GAME_OVER
                else:
                    wrongGuesses = g.wrong.difference(g.guesses)
                    if wrongGuesses:
                        payload = '\n'.join([g.blanks, sorted(list(wrongGuesses))])
                    else:
                        payload = g.blanks
                    resp.message(payload)
            finally:
                save_game(g)

    # game over
    if state == StateMachine.GAME_OVER:
        g = load_game()
        resp.message("Congrats, the word was {}!".format(g.answer))
        resp.message("Text 'new game' to play again!")
        state = StateMachine.FIRST_TIME_LOAD
    # player LATER
    elif state == StateMachine.LATER:
        resp.message("Oh, okay- text 'new game' any time to play again!")
        state = StateMachine.FIRST_TIME_LOAD

    # send message(s)
    session['gameState'] = state
    return str(resp)


if __name__ == '__main__':
    app.run()
