from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for sessions; change this to a secure key in production

# File to store messages
MESSAGE_FILE = "messages.txt"

# Ensure the messages file exists
if not os.path.exists(MESSAGE_FILE):
    with open(MESSAGE_FILE, "w") as f:
        pass

# Hardcoded password (change this in production)
PASSWORD = "Coaching4050"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    mobile = request.form['mobile']
    email = request.form['email']
    message = request.form['message']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(MESSAGE_FILE, "a") as f:
        f.write(f"Name: {name}\nMobile: {mobile}\nEmail: {email}\nMessage: {message}\nTimestamp: {timestamp}\n---\n")
    
    print(f"Contact Form Submission: {name}, {mobile}, {email}, {message}")
    return redirect(url_for('home') + '#contact')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('messages'))
        else:
            return render_template('login.html', error="Incorrect password. Please try again.")
    return render_template('login.html', error=None)

@app.route('/messages')
def messages():
    print("Messages route accessed")
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    messages = []
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as f:
            content = f.read().strip()
            if content:
                message_blocks = content.split("---\n")
                for block in message_blocks:
                    if block.strip():
                        lines = block.strip().split("\n")
                        message_dict = {}
                        for line in lines:
                            if ": " in line:
                                key, value = line.split(": ", 1)
                                message_dict[key] = value
                        if message_dict:
                            messages.append((
                                message_dict.get("Name", ""),
                                message_dict.get("Mobile", ""),
                                message_dict.get("Email", ""),
                                message_dict.get("Message", ""),
                                message_dict.get("Timestamp", "")
                            ))
    
    messages.sort(key=lambda x: x[4], reverse=True)
    
    return render_template('messages.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)