from datetime import datetime

from flask import Flask, render_template, redirect, request, url_for, session
import flaskext.sqlalchemy as sqla
from flaskext.wtf import Form, PasswordField, HiddenField, TextField, Required

SECRET_KEY = 'dev_key' # in a real project, this should be random.

# Create Flask application object
app = Flask(__name__)

# Configure flask & sqlalchemy to use a sqlite database & create that database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blabber.db'
db = sqla.SQLAlchemy(app)

# VIEWS #

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id', None)
    raise
    if user_id:
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        login_form = LoginForm()
        add_user_form = AddUserForm()
        return render_template('login.html', login_form=login_form, add_user_form=add_user_form)
    else:
        form = LoginForm()
        try:
            user = User.query.filter_by(name=form.username.data).one()
            if user.password == form.password.data:
                session['user_id'] = user.id
        except Exception, e:
            print e

        return redirect(url_for('home'))

@app.route("/logout")
def logout():
    if session.get('user_id', None):
        session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route("/")
def home():
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect(url_for('login'))

    blabs = db.session.query(Blab). \
        filter(Creep.creeper_id==user_id). \
        filter(Blab.user_id==Creep.creepee_id).\
        all()
    blab_form = BlabForm()
    
    return render_template('blabs.html', blabs=blabs, blab_form=blab_form)

@app.route('/user/<user_id>')
def show_user(user_id):
    user = User.query.filter_by(id=user_id).one()
    blabs = Blab.query.filter_by(user_id=user_id).all()
    return render_template('user.html', blabs=blabs, user=user)

@app.route("/users")
def show_users():
    users = User.query.all()
    creeped_users = db.session.query(User). \
        filter(User.id==Creep.creepee_id). \
        filter(Creep.creeper_id==session['user_id']).all() 
    return render_template('users.html', users=users, creeped_users=creeped_users)

@app.route("/add_blab", methods=['POST'])
def add_blab():
    form = BlabForm()

    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).one()
  
    new_blab = Blab(form.blab.data, user)
    
    db.session.add(new_blab)
    db.session.commit()
  
    return redirect(url_for('home'))

@app.route("/add_user", methods=['POST'])
def add_user():
    form = AddUserForm()
    new_user = User(form.username.data, form.password.data)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/creep_user", methods=['POST'])
def creep_user():
    # don't do anything if we're not logged in.
    user_id = session.get('user_id', None)
    if user_id:
        form = CreepForm()
        creepee_id = form.user_id.data
        creeper_id = user_id

        new_creep = Creep(creeper_id, creepee_id)
        db.session.add(new_creep)
        db.session.commit()

    return redirect(url_for('show_users'))

@app.route("/uncreep_user", methods=['POST'])
def uncreep_user():
    # don't do anything if we're not logged in.
    user_id = session.get('user_id', None)
    if user_id:
        form = CreepForm()
        try:
            creep = Creep.query.filter_by(creeper_id=user_id, creepee_id=form.user_id.data).one()
            db.session.delete(creep)
            db.session.commit()
        except Exception, e:
            print e

    return redirect(url_for('show_users'))

# FORMS #

class BlabForm(Form):
    blab = TextField('blab', validators=[Required()])

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

class AddUserForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])

class CreepForm(Form):
    user_id = HiddenField('user_id', validators=[Required()])

class UnCreepForm(Form):
    user_id = HiddenField('user_id', validators=[Required()])

# MODELS #

class Blab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('blab', lazy='dynamic'))

    time = db.Column(db.DateTime)
    text = db.Column(db.String())

    def __init__(self, text, user, time=datetime.utcnow()):
        self.user = user
        self.time = time
        self.text = text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80)) # THIS PASSWORD IS STORED IN PLAIN TEXT. THIS IS BAD.

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User Obj: %s>" % self.name

class Creep(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creeper_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creepee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, creeper_id, creepee_id):
        self.creeper_id = creeper_id
        self.creepee_id = creepee_id

    def __repr__(self):
        creeper = User.query.filter_by(id=self.creeper_id).one()
        creepee = User.query.filter_by(id=self.creepee_id).one()
        return "<Creep Obj: %s is creepin on %s>" % (creeper.name, creepee.name)

# OTHER #

if __name__ == "__main__":
    db.create_all()
    app.secret_key = SECRET_KEY
    app.run(host='0.0.0.0.', port=8080, debug=True)
