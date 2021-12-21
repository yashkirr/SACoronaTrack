import flask
import tweeterBot

app = flask.Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return "@SACoronaTracker Home"

#create a app.route for a config page.
@app.route("/config")
def config():
    tweeterBot.main()
    return "@SACoronaTracker Config"

if __name__ == '__main__': 
    app.run(debug=True)