import env
from hangman import *
from state_machine import *
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
)

class Keywords:
    HELLO = "HELLO"
    NEW_GAME = "NEW GAME"
    LATER = "LATER"

class SessionKeys:
    GAME_DATA = 'gameData'
    STATE_DATA = 'stateData'


def save_game(game):
    session[SessionKeys.GAME_DATA] = game.to_json()
def load_game():
    return HangmanGame.from_json(session[SessionKeys.GAME_DATA])


@app.route('/sms', methods=['POST'])
def sms_reply():
    # retrieve game state
    try:
        state = session[SessionKeys.STATE_DATA]
    except KeyError:
        state = StateMachine.FIRST_TIME_LOAD

    # retrieve user's message and prepare response
    msg = request.form['Body'].upper().strip()
    resp = MessagingResponse()

    # first time load
    if state == StateMachine.FIRST_TIME_LOAD:
        if Keywords.NEW_GAME in msg:
            state = StateMachine.NEW_GAME
        elif Keywords.HELLO in msg:
            resp.message("Hello! Text 'new game' to play.")

    # new game
    if state == StateMachine.NEW_GAME:
        resp.message("Starting a new game. Text a letter or word to guess, or text 'later' to stop.")
        g = HangmanGame()
        resp.message(g.blanks)
        save_game(g)
        state = StateMachine.IN_PROGRESS
    # in progress
    elif state == StateMachine.IN_PROGRESS:
        g = load_game()
        if Keywords.LATER in msg:
            state = StateMachine.LATER
        else:
            try:
                g.sanitize_guess(msg)
            except InvalidGuessError:
                if msg == g.answer:
                    state = StateMachine.GAME_OVER
                else:
                    resp.message("Whoops- I didn't understand your guess! Try again.")
            except LetterAlreadyGuessedError:
                resp.message("Whoops- you already guessed that letter! Try again.")
            else:
                if g.guess(msg):
                    state = StateMachine.GAME_OVER
                else:
                    wrongGuesses = sorted(list(g.guesses.intersection(g.wrong)))
                    if wrongGuesses:
                        payload = '\n'.join([g.blanks, ', '.join(wrongGuesses)])
                    else:
                        payload = g.blanks
                    resp.message(payload)
                    if g.max_wrong_exceeded():
                        resp.message("Uh oh- you're all out of guesses! What's the word?")
                        state = StateMachine.FINAL_GUESS
            finally:
                save_game(g)
    # final guess
    elif state == StateMachine.FINAL_GUESS:
        # separate state used to bypass LATER recognition and guess sanitizaiton
        state = StateMachine.GAME_OVER

    # game over
    if state == StateMachine.GAME_OVER:
        g = load_game()
        if g.answer == msg or not g.max_wrong_exceeded():
            reaction = "Congrats"
        else:
            reaction = "Sorry"
        resp.message("{}, the word was {}!".format(reaction, g.answer))
        resp.message("Text 'new game' to play again!")
        state = StateMachine.FIRST_TIME_LOAD
    # player LATER
    elif state == StateMachine.LATER:
        resp.message("Oh, okay- text 'new game' any time to play again!")
        state = StateMachine.FIRST_TIME_LOAD

    # send message(s)
    session[SessionKeys.STATE_DATA] = state
    return str(resp)


if __name__ == '__main__':
    app.run()
