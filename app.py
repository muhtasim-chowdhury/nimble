import os

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# test global variable

# test = "hello";
server = dict()



@app.route("/")
def index():

	return render_template('index.html')


@app.route("/channels", methods=["POST"])
def channels():
	name = request.form.get('user')
	if name:
		# user enters for first time
		# check if user list exists
		try:
			# add user if user does not exist in list
			if not name in server['users']:
				server['users'].append(name)
		except KeyError:
			# if list doesn't exist, create and add user
			server['users'] = []
			server['users'].append(name)
		except:
			return "you dun goofed"

		# log user in
		session['current_user'] = name
		# return render_template('channels.html', cur=session['current_user'])

	else:

		# create a channel
		try:
			server['channels']
		except:
			server['channels'] = []


		if len(server['channels']) == 0:
			# create channel list of dicts
			server['channel_count'] = 0
			count = server['channel_count']
			server['channels'].append({ 'name': str(count) , 'messages': []})
			# return render_template('channels.html', channels=session['channels'])

		else:
			# list already exists so just create add another channel
			server['channel_count'] += 1 
			count = server['channel_count']
			server['channels'].append({ 'name': str(count) , 'messages': []})


	try:
		return  render_template('channels.html', channels=server['channels'], cur=session['current_user'])
	except KeyError:
		return  render_template('channels.html', cur=session['current_user'])
		# jsonify(session['channels'])



@app.route("/channels/<string:channel>")
def channel(channel):

	channel_num = int(channel)
	# list of messages 
	messages = server['channels'][channel_num]['messages']

	
	return render_template('chat.html', user=session['current_user'], messages=messages, channel_num=channel_num)


@socketio.on("message sent")
def message(info):
	message = info['m']
	user = info['u']
	channel_num = info['channel_num']
	channel_num = int(channel_num)
	time = info['time']
	
	# add message to messages list to the CORRECT CHANNEL
	server['channels'][channel_num]['messages'].append( user + ": " + message +" Time: " + time)


	emit('display message', {"new": message, 'user': user, 'channel_num': channel_num, 'time': time}, broadcast=True)