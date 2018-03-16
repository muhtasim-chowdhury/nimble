import os

from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# configure session
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# session is a dict


@app.route("/")
def index():

	# clear all channels
	session['channel_count'] = 1
	session['channels'].clear()
	return render_template('index.html')


@app.route("/channels", methods=["POST"])
def channels():
	name = request.form.get('user')
	if name:
		# user enters for first time
		# check if user list exists
		try:
			# add user if user does not exist in list
			if not name in session['users']:
				session['users'].append(name)
		except KeyError:
			# if list doesn't exist, create and add user
			session['users'] = []
			session['users'].append(name)
		except:
			return "you dun goofed"

		# log user in
		session['current_user'] = name
		# return render_template('channels.html', cur=session['current_user'])

	else:

		# create a channel
		if len(session['channels']) == 0:
			# create channel list of dicts
			session['channels'] = []
			session['channel_count'] = 1
			count = session['channel_count']
			session['channels'].append({ 'name': 'channel ' + str(count) , 'messages': []})
			# return render_template('channels.html', channels=session['channels'])

		else:
			# list already exists so just create add another channel
			session['channel_count'] += 1 
			count = session['channel_count']
			session['channels'].append({ 'name': 'channel ' + str(count) , 'messages': []})



	return  render_template('channels.html', channels=session['channels'], cur=session['current_user'])
		# jsonify(session['channels'])


@app.route("/channels/<string:channel>")
def channel(channel):
	return render_template('chat.html')