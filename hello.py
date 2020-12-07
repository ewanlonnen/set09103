import bcrypt
import sqlite3
from functools import wraps
from flask import Flask , request, redirect, render_template, request, session, url_for, g
from flask import Flask
app = Flask ( __name__ )
db_location = 'var/logins.db'
email = ""

def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = sqlite3.connect(db_location)
		g.db = db
	return db

@app.teardown_appcontext
def close_db_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('logins.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
@app.route("/register/", methods =['GET', 'POST'])
def register():
	session['logged in'] = False
	if request.method == 'POST':
		user = request.form['email']
		pw = request.form['password']
		if (user == ""):
			return render_template('register.html')
		if (pw == ""):
			return render_template('register.html')
		db = get_db()
		hash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
		hash = hash.decode('utf-8')
		insert = "insert into details values('%s', '%s')" % (user, hash)
		db.cursor().execute(insert)
		db.commit()
		return redirect(url_for('.root'))
		session['logged in'] = True
	return render_template('register.html')

@app.route("/spit_db/")
def spit():
	db = get_db()
	page = []
	page.append('<html>')
	page.append(email)
	page.append('<ul>')
	sql = "SELECT * FROM details"
	for row in db.cursor().execute(sql):
		page.append('<li>')
		page.append(str(row))
		page.append('</li>')
	page.append('</ul></html>')
	return ''.join(page)

app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
def check_auth(email,password):
	db = get_db()
	result = ""
	test_pwd = "SELECT pw FROM details WHERE user = '%s'" % (email)
	for row in db.cursor().execute(test_pwd):
		result = result + (str(row))
	result = result[2:-3]
	if (result == ""):
		return False
	if (bcrypt.checkpw(password.encode('utf-8'), result.encode('utf-8'))):
		return True
	else:
		return False
def requires_login(f):
        @wraps(f)
        def decorated(*args, **kwargs):
                status = session.get('logged_in', False)
                if not status:
                        return redirect(url_for('.root'))
                return f (*args, **kwargs)
        return decorated

@app.route('/logout/')
def logout ():
        session['logged_in']= False
        return redirect(url_for('.root'))

@app.route("/", methods =['GET', 'POST'])
def root():
	if request.method == 'POST':
		user = request.form['email']
		pw = request.form['password']
		test3456 = ""
		test3456 = check_auth(request.form['email'],request.form['password'])
		if check_auth(request.form['email'],request.form['password']):
			session['logged_in'] = True
			return render_template('main.html')
		else:
			return render_template('invalid.html')
	return render_template('login.html')

@app.route ("/help/", methods=['POST', 'GET'])
def account () :
	if request.method == 'POST':
		print(request.form)
		name = request.form['name']
		return " Hello %s" % name
	else:
		page = '''
		<html><body>
		<form action="" method ="post" name ="form">
		<label for="name" > Name : </label>
		<input type="text" name="name" id ="name"/>
		<input type="submit" name="submit" id ="submit "/>
		</form>
		</body><html> '''
	return page

@app.route('/secret/')
@requires_login
def inheritance():
	return render_template('main.html')

@app.route('/secret/castle1/')
@requires_login
def castle1():
	return render_template('castle1.html')

@app.route('/secret/castle2/')
@requires_login
def castle2():
	return render_template('castle2.html')
@app.route('/secret/stmary1/')
@requires_login
def stmary1():
	return render_template('stmary1.html')
@app.route('/secret/stmary2/')
@requires_login
def stmary2():
	return render_template('stmary2.html')
@app.route('/secret/spire1/')
@requires_login
def spire1():
	return render_template('spire1.html')
@app.route('/secret/spire2/')
@requires_login
def spire2():
	return render_template('spire2.html')
@app.route('/secret/balmoral1/')
@requires_login
def balmoral1():
	return render_template('balmoral1.html')
@app.route('/secret/balmoral2/')
@requires_login
def balmoral2():
	return render_template('balmoral2.html')
if __name__ == " __main__ ":
	app.run (host ='0.0.0.0', debug = True )
