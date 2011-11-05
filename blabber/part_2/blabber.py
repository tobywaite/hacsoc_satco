from flask import Flask

app = Flask(__name__)

# Endpoint for the Blabber homepage.
@app.route("/")
def home():
    return "This is the main blabber homepage!"

# add routes and function definitions for the other endpoints we will need for Blabber.

if __name__ == "__main__":
    app.run(host='0.0.0.0.', port='8080', debug=True)
