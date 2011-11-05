from datetime import datetime

from flask import Flask, render_template, redirect, request, url_for, session
import flaskext.sqlalchemy as sqla
from flaskext.wtf import Form, PasswordField, HiddenField, TextField, Required

# APP SETUP #

SECRET_KEY = 'dev_key' #in a real project, this should be random. And secret.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blabber.db'
app.secret_key = SECRET_KEY
db = sqla.SQLAlchemy(app)

# ROUTING #

@app.route("/")
def home():

    blabs = Blab.query.all()
    blab_form = BlabForm()

    return render_template("blabs.html", blabs=blabs, blab_form=blab_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    add_user_form = AddUserForm()

    return render_template("login.html", add_user_form=add_user_form)

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
    form = AddUserForm()
    new_user = User(form.username.data, form.password.data)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/add_blab", methods=['POST'])
def add_blab():
    form = BlabForm()

    new_blab = Blab(form.blab.data)

    db.session.add(new_blab)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/creep_user", methods=['POST'])
def creep_user():
    return "This endpoint will allow users to creep (follow) new users"

@app.route("/uncreep_user", methods=['POST'])
def uncreep_user():
    return "This endpoint will allow users to uncreep (unfollow) new users"

# FORMS #

class BlabForm(Form):
    blab = TextField('blab', validators=[Required()])

# This form lets a user submit their user name and password to log in.
class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

# We just added a form here to allow a user to create a new username with a password!
class AddUserForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('username', validators=[Required()])

class CreepForm(Form):
    user_id = HiddenField('user_id', validators=[Required()])

class UnCreepForm(Form):
    user_id = HiddenField('user_id', validators=[Required()])

# DATABASE MODELS # 

# The user model is used to store our Blabber users in our database
class User(db.Model):
    # The 'id' field uniquely identifies each user in the database
    id = db.Column(db.Integer, primary_key=True)
    
    # the 'name' field holds a user's username
    name = db.Column(db.String(80))
    
    # the 'password' field holds a users password, so we can check it when they try to log in. 
    # Note: Here, we store the password in plain text. This is unacceptably bad security practice.
    password = db.Column(db.String(80))

    # the '__init__' method initializes new database objects when we create them.
    # The ID field will be populated automatically, so we only need to populated the other two.
    def __init__(self, name, password):
        self.name = name
        self.password = password

# The Blab model stores the actual Blabs in the database
class Blab(db.Model):
    # The id field uniquely identifies each Blab in the database
    id = db.Column(db.Integer, primary_key=True)

    # We want to know when each blab was posted, so we store that here.
    time = db.Column(db.DateTime)
    # This stores the actual text of the blab.
    text = db.Column(db.String())

    # For this, we've decided not to deal with users.

    # We store the user_id for the user who posted the blab
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # This mumbo-jumbo tells the database that the user_id references a user in the 'User' table
    #user = db.relationship('User',
    #    backref=db.backref('back', lazy='dynamic'))

    # When creating a new blab object, we must initialize it. This allows us to specify default values if wanted.
    def __init__(self, text, time=datetime.utcnow()):
        self.text = text
        #self.user = user
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
