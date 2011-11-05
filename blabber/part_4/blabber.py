from datetime import datetime

from flask import Flask, render_template
import flaskext.sqlalchemy as sqla

# APP SETUP #

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blabber.db'
db = sqla.SQLAlchemy(app)

# ROUTING #

@app.route("/")
def home():

    # We create a list of blabs to pass to the template
    blabs = [
        "This is a test blab",
        "Toby can Blab all day long!",
        "Check out this sweet Blab",
        "Python python python python BADGER"]

    return render_template("blabs.html", blabs=blabs)

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/logout", methods=['POST'])
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

# DATABASE MODELS # 

# The user model is used to store our Blabber users in our database
class User(db.Model):
    # using the other models (below) as an example, create the User model for Blabber.
    pass

# The Blab model stores the actual Blabs in the database
class Blab(db.Model):
    # The id field uniquely identifies each Blab in the database
    id = db.Column(db.Integer, primary_key=True)

    # We want to know when each blab was posted, so we store that here.
    time = db.Column(db.DateTime)
    # This stores the actual text of the blab.
    text = db.Column(db.String())

    # We store the user_id for the user who posted the blab
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # This mumbo-jumbo tells the database that the user_id references a user in the 'User' table
    user = db.relationship('User',
        backref=db.backref('back', lazy='dynamic'))

    # When creating a new blab object, we must initialize it. This allows us to specify default values if wanted.
    def __init__(self, text, user, time=datetime.utcnow()):
        self.text = text
        self.user = user
        self.time = time

# The creep model keeps track of who is creeping on (following) whom
class Creep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    # This stores the user ID of the user who is being a creep.
    creeper_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Similarly, this stores the user ID of the user who is being creeped upon.
    creepee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #initialize the Creep model
    def __init__(self, creeper_id, creepee_id):
        self.creeper_id = creeper_id
        self.creepee_id = creepee_id
    
if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
