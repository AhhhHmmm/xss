from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/admin/desktop/PostAP/Lesson2/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.autoescape = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), unique=True)
	password = db.Column(db.String)

	def __repr__(self):
		return f'<User username={username}, password={password}'
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40))
	message = db.Column(db.String)

class SignUpForm(FlaskForm):
	username = StringField(label='Username', validators=[InputRequired(), Length(max=40)])
	password = PasswordField(label='Password', validators=[InputRequired(), Length(max=80)])

class LoginForm(FlaskForm):
	username = StringField(label='Username', validators=[InputRequired(), Length(max=40)])
	password = PasswordField(label='Password', validators=[InputRequired(), Length(max=80)])

@app.route('/')
def index():
	posts = db.session.query(Post).all()
	return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			user = db.session.query(User).filter(User.username == form.username.data).first()
			if user:
				hashed_password = hashlib.sha256(str.encode(form.password.data)).hexdigest()
				if hashed_password == user.password:
					return 'Logged in!'
		return 'Login Error, password incorrect!'
	else:
		return render_template('login.html', form=form) 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	
	if request.method == 'POST':
		if form.validate_on_submit():
			hashed_password = hashlib.sha256(str.encode(form.password.data)).hexdigest()
			new_user = User(username=form.username.data, password=hashed_password)
			db.session.add(new_user)
			db.session.commit()
			return 'New user added to database!'
	else:
		return render_template('signup.html', form=form)

@app.route('/database_view')
def database_view():
	users = db.session.query(User).all()
	return render_template('database_view.html', users=users)

@app.route('/process_post', methods=['POST'])
def process_post():
	username = request.form['username']
	message = request.form['message']

	post = Post(username=username, message=message)
	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))

# if __name__ == "__main__":
# 	app.run(debug=True)