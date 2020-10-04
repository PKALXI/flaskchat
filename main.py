from flask import *
from flask_socketio import SocketIO, send


app = Flask('__main__')
socketio = SocketIO(app)

#encrypt data
app.secret_key = "jaiMataDi"

@socketio.on('message')
def handle_message(msg):
    print('activated')

    if msg == 'entered':
        send(f'{session["username"]} has entered', broadcast=True)
    else:
        send(f'{session["username"]}: {msg}', broadcast=True)


@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['nm']
        session['username'] = username
        #send_username()
        return redirect(url_for('chat'))
    else:
        if 'username' in session:
            #send_username()
            return redirect(url_for('chat'))
        return render_template('login.html')

@app.route('/chat', methods = ['POST', 'GET'])
def chat():
    return render_template('chat.html', name=session['username'])

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    socketio.run(app)