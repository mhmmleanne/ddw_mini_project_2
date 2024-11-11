from app import application, db #import our database
from app.models import User, Question, Challenge, TimeRecord #imports all your database tables

@application.shell_context_processor #allowing u to run a py shell when typing flask shell
def make_shell_context(): #assign your attributes with these classes
	return {'db': db, 'User': User, 'Question': Question,
			'Challenge': Challenge,
			'TimeRecord': TimeRecord}

if __name__ == "__main__": #run ur application 
	application.run(host="0.0.0.0", port=8080, debug=True)
