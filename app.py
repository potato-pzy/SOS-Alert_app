from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Add static folder for audio files
app.config['AUDIO_FOLDER'] = os.path.join(app.static_folder, 'audio')
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Ensure audio folder exists
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    emergency_contact = db.Column(db.String(80), nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Add route to serve audio files
@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        emergency_contact = request.form['emergency_contact']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, emergency_contact=emergency_contact)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('sos_alert')
def handle_sos(data):
    username = session.get('username')
    if username:
        user = User.query.filter_by(username=username).first()
        if user and user.emergency_contact:
            # Emit to all connected clients
            emit('sos_notification', {
                'username': username,
                'emergency_contact': user.emergency_contact,
                'play_alert': True  # Add flag to trigger sound
            }, broadcast=True)
            return {'status': 'success'}
    return {'status': 'error'}

if __name__ == '__main__':
    socketio.run(app, debug=True)