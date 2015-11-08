import urllib.parse as urlparse
from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth
# from flask.ext.social import Social

print(dir(OAuth.__module__))

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = 'SECRET'
FACEBOOK_APP_SECRET = 'SECRET'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

app = Flask(__name__)
facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': 'email'})

@app.route("/")
def index():
	return redirect(url_for('login'))

@app.route('/login')
def login():
	print("something")
	return facebook.authorize(
		callback=url_for('facebook_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	print(resp)
	if resp is None:
		return 'Access denied: reason=%s error=%s' % (
			request.args['error_reason'],
			request.args['error_description']
		)
	session['oauth_token'] = (resp['access_token'], '')
	me = facebook.get('/me')
	return 'Logged in as id=%s name=%s redirect=%s' % \
		(me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('oauth_token')



# @app.route("/")
# def login():
#     return render_template(
#         'login.html',
#         content='Posts Page',
#         facebook_conn=social.facebook.get_connection())



if __name__ == "__main__":
	app.run()