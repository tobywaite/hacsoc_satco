from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Blabber!"

@app.route("/second_page")
def second_page():
    return "This is a second page!"

if __name__ == "__main__":
    app.run(host='0.0.0.0.', port='8080', debug=True)
