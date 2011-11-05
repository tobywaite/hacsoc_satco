from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():

    # We create a list of blabs to pass to the template
    blabs = [
        "This is a test blab",
        "Toby can Blab all day long!",
        "Check out this sweet Blab",
        "Python python python python BADGER"]

    return render_template("blabs.html", blabs=blabs)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return "Visiting this page will log a user out."

@app.route("/users")
def show_users():
    return render_template("users.html")

@app.route("/user/<user_id>")
def show_user(user_id):
    return render_template("user.html")

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
