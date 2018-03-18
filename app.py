import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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

# message id needed to delete them
message_id = 0





@app.route("/")
def index():	
	# if session['current_channel']:
	# 	return redirect(url_for('channel', channel=session['current_channel']) )
	# else:
	# 	return render_template('index.html')
	if 'channels' in server: 
		try:
			return redirect(url_for('channel', channel=session['current_channel']) )
		except KeyError:
			return render_template('index.html')
		except:
			return 'you dun goofed'
	else:
		return render_template('index.html')




@app.route("/channels", methods=["POST", "GET"])
def channels():
	# coming from channel page
	if request.method == 'GET':
		return render_template('channels.html', channels=server['channels'], cur=session['current_user'])
	else:
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
	# get channel id
	channel_num = int(channel)

	# remember channel id as a cookie
	session['current_channel'] = channel_num


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
	# server['channels'][channel_num]['messages'].append( user + ": " + message +" Time: " + time)
	global message_id
	server['channels'][channel_num]['messages'].append( {'user': user, 'message': message, 'time': time, 'id': message_id})
	message_id += 1
	emit('display message', {"new": message, 'user': user, 'channel_num': channel_num, 'time': time, 'id': message_id}, broadcast=True)

@app.route("/fuck")
def fuck():
	return str(session['current_channel'])



@app.route("/delete", methods=["POST"])
def delete():
	idd = int(request.form.get('id'))
	channel = int(request.form.get('channel'))
	


	for i in range(len(server['channels'][channel]['messages'])):
	# for item in server['channels'][channel]['messages']:
		# if item.id == idd:
		if server['channels'][channel]['messages'][i]['id'] == idd:
			
			server['channels'][channel]['messages'].remove(server['channels'][channel]['messages'][i])
			return 
			# "success"
		
	return 
	# "not found"





	# delete message
