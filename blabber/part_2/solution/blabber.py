from flask import Flask

app = Flask(__name__)

# Endpoint for the Blabber homepage.
@app.route("/")
def home():
    return "This is the main blabber homepage!"

@app.route("/login", methods=['GET', 'POST'])
def login():
    return "This is the login page"

@app.route("/logout", methods=['POST'])
def logout():
    return "Visiting this page will log a user out."

@app.route("/users")
def show_users():
    return "This page will show all users on Blabber"

@app.route("/user/<user_id>")
def show_user(user_id):
    return "This page will show a particular user's profile"

@app.route("/add_user", methods=['POST'])
def add_user():
    return "This endpoint will allow us to add new users to Blabber"

@app.route("/add_blab", methods=['POST'])
def add_blab():
    return "This endpoint will allow users to post new blabs"

@app.route("/creep_user", methods=['POST'])
def creep_user():
    return "This endpoint will allow users to creep (follow) new users"

@app.route("/uncreep_user", methods=['POST'])
def uncreep_user():
    return "This endpoint will allow users to uncreep (unfollow) new users"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
