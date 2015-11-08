from flask import Flask
from flask.ext.social import Social

app = Flask(__name__)

@app.route("/")
def hello():
    # return "Hello World!"
    return render_template(
        'profile.html',
        content='Profile Page',
        facebook_conn=social.facebook.get_connection())

# @app.route('/profile')
# def profile():
#     return render_template(
#         'profile.html',
#         content='Profile Page',
#         facebook_conn=social.facebook.get_connection(),

if __name__ == "__main__":
	app.run()