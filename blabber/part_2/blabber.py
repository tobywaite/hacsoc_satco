from flask import Flask
import flaskext.sqlalchemy as sqla
from flaskext.wtf import Form, TextField, Required

# Create Flask application object
app = Flask(__name__)

# Configure flask & sqlalchemy to use a sqlite database & create that database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blabber.db'
db = sqla.SQLAlchemy(app)

# VIEWS #

@app.route("/")
def home():
    if not session.user_id:
        return redirect(url_for('login'))


    blab_form = BlabForm()
    
    return render_template('blabs.html', blabs=blabs, blab_form=blab_form)

@app.route("/user/<user_id>")
def show_user():
    blabs = Blab.query.filter_by(Blab.user_id=user_id).all()
    creeped_users = User.query.all() # TODO: This should return just the creeped users (join against creep)
    return render_template('user.html', blabs=blabs, creeped_users=creeped_users)

@app.route("/users")
def show_users():
    users = Users.query.all()
    return render_template('users.html', users=users)

@app.route("/add_blab", methods=['POST'])
def add_blab():
    form = BlabForm()
    new_blab = Blab(form.blab)
    db.session.add(new_blab)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add_user", methods=['POST'])
def add_user():
    form = UserForm()
    new_user = User(form.username, form.password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/creep_user", methods=['POST'])
def creep_user():
    # don't do anything if we're not logged in.
    if session.user_id:
        form = CreepForm()
        creepee_id = form.user_id
        creepee = User.query.filter_by(id = creepee_id).one()
        creeper_id = session.user_id
        creeper = User.query.filter_by(id = creeper_id).one()

        new_creep = Creep(creepee, creeper)
        db.session.add(new_creep)
        db.session.commit()

    return redirect(url_for('home'))

@app.route("/uncreep_user", methods=['POST'])
def uncreep_user():
    # don't do anything if we're not logged in.
    if session.user_id:
        form = CreepForm()
        try:
            creep = Creep.query.filter_by(creeper_id=session.user_id, creepee_id=form.user_id).one()
            db.session.delete(creep)
        except Exception, e:
            print e

    return redirect(url_for('home'))

# FORMS #

def BlabForm(Form):
    blab = TextField(blab, validators=[Required()])

def CreepForm(Form):
    user_id = TextField(blab, validators=[Required()])

def UnCreepForm(Form):
    user_id = TextField(blab, validators=[Required()])

def UserForm(Form):
    username = TextField(username, validators=[Required()])
    password = TextField(password, validators=[Required()])

# MODELS #

def Blab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User',
        backref=db.backref('blab', lazy='dynamic'))

    time = db.Column(db.DateTime)
    text = db.Column(db.String())

    def __init__(self, text, time=datetime.utcnow()):
        self.time = time
        self.text = text

def User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80)) # THIS PASSWORD IS STORED IN PLAIN TEXT. THIS IS BAD.

    def __init__(self, name, password):
        self.name = name
        self.password = password

def Creep(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creeper_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creeper = db.relationship('User',
        backref=db.backref('creep', lazy='dynamic'))

    creepee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creepee = db.relationship('User',
        backref=db.backref('creep', lazy='dynamic'))

# OTHER #

if __name__ == "__main__":
    app.run(host='0.0.0.0.', port='8080')
