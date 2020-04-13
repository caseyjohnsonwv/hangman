import env
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
)

@app.route('/sms', methods=['POST'])
def sms_reply():
    player_number = request.form['From']
    resp = MessagingResponse()
    resp.message("Hello, {}!".format(player_number))
    return str(resp)

if __name__ == '__main__':
    app.run()
