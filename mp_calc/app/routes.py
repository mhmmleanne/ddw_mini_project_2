from app import application
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, CreateQuestionForm, ChallengeAnswerForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question, Challenge, TimeRecord
from urllib.parse import urlparse, unquote
from app import db
from flask import request 
from app.serverlibrary import mergesort, EvaluateExpression, get_smallest_three 


@application.route('/')
@application.route('/index/') #url of the home page
@login_required #force user to login to access other pages
def index():
	prefix = application.wsgi_app.prefix[:-1]
	return render_template('index.html', title='Home', prefix=prefix) #render ur css

@application.route('/users/') #url of the users page
@login_required #force user to login to access
def users():
	prefix = application.wsgi_app.prefix[:-1]
	users = User.query.all()	 
	#retrives all users from the database, stuff it into User table located in models.py
	mergesort(users, lambda item: item.username) 
	#calls sorting function to sort list of users alphabetically using username atttibute
	usernames = [u.username for u in users]
	#create a list of usernames
	return render_template('users.html', title='Users',
							users=usernames, prefix=prefix) #put css

@application.route('/questions/', methods=['GET','POST']) #url of the questions page
@login_required #force user to login to access
def questions():
	prefix = application.wsgi_app.prefix[:-1]
	questions = current_user.questions.all() #displays all questions for the user
	form = CreateQuestionForm() #the form to let user type in
	users = User.query.all() #provide a list of all possible users person can assign question to 
	userlist = [(u.username, u.username) for u in users] 
	form.assign_to.choices=userlist 
	if form.validate_on_submit(): #if question is valid
		question = Question(expression=form.expression.data) #assign a Question class to the string provided by the user
		evalans = EvaluateExpression(form.expression.data) #create an empty box to answer the question
		question.answer = evalans.evaluate() #evulate answer given by user
		question.author = current_user.id #show author of question
		challenge = Challenge(question=question) 
		username_to = []
		for name in form.assign_to.data: #filter all users, find the person u assigned to and give the question to them
			username_to.append(User.query.filter_by(username=name).first())

		challenge.to_user = username_to
		db.session.add(question) #add question to database
		db.session.add(challenge) #add challenge to database
		db.session.commit() #ensure got changes
		flash('Congratulations, you have created a new question.') #tell user they sucessfully entered a question
		questions = current_user.questions.all() #update and show all questions given by user
	return render_template('questions.html', title='Questions', 
							user=current_user,
							questions=questions,
							form=form, prefix=prefix) #render css

@application.route('/challenges/', methods=['GET', 'POST']) #url for challenges pages
@login_required #force user to login to access
def challenges():
	prefix = application.wsgi_app.prefix[:-1]
	challenges = current_user.challenges.all() #show all challenges 
	form = ChallengeAnswerForm() #create form to answer
	recordsquery = TimeRecord.query.filter_by(user_id=current_user.id).all() #find data for timing on challenge based on user
	records = { c.id: r.elapsed_time for r in recordsquery for c in challenges if r.challenge_id== c.id}
	#show how long it took for each challenge
	if form.validate_on_submit(): #if user inputted into form
		record = TimeRecord() #record the data once u press show q
		record.elapsed_time = int(form.elapsed_time.data) #get data
		record.challenge_id = int(form.challenge_id.data) #get data
		record.user_id = current_user.id #record the person who pressed button
		answer = form.answer.data #get anseer data
		challenge = Challenge.query.filter_by(id=form.challenge_id.data).first()
		if int(answer) == int(challenge.question.answer): #check whether data is properly stored or smth
			db.session.add(record) #add it into the database
			db.session.commit() #make sure its the databse
			challenges = current_user.challenges.all()  #show all challenges assigned to user
			recordsquery = TimeRecord.query.filter_by(user_id=current_user.id).all()
			records = { c.id: r.elapsed_time for r in recordsquery for c in challenges if r.challenge_id== c.id}
			form.answer.data = ""
			return render_template('challenges.html', title='Challenges',
							user=current_user,
							challenges=challenges,
							form = form,
							records = records, prefix=prefix)
		
		return redirect(url_for('challenges'))
	form.answer.data=""
	return render_template('challenges.html', title='Challenges',
							user=current_user,
							challenges=challenges,
							form = form,
							records = records, prefix=prefix)

@application.route('/halloffame/')
def halloffame():
	prefix = application.wsgi_app.prefix[:-1]
	challenges = Challenge.query.all()
	records = { c.id:get_smallest_three(c) for c in challenges}
	print(records)
	return render_template('halloffame.html', title="Hall of Fame",
							challenges=challenges,
							records=records, prefix=prefix)

@application.route('/login/', methods=['GET', 'POST'])
def login():
	prefix = application.wsgi_app.prefix[:-1]
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		if (request.args.get('next')) is None:
			next_page = None
		else:
			next_page = unquote(request.args.get('next'))

		if not next_page or urlparse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form, prefix=prefix)

@application.route('/logout/')
def logout():
	prefix = application.wsgi_app.prefix[:-1]
	logout_user()
	return redirect(url_for('index'))

@application.route('/register/', methods=['GET', 'POST'])
def register():
	prefix = application.wsgi_app.prefix[:-1]
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user.')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form, prefix=prefix)

