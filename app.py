import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_secure_key_123'  
#for security

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if folder not exist create a folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# security and access control 
USERS = {
    "admin@trustvalet.com": "admin123",
    "user@trustvalet.com": "user123"
}

# --- AUDIT TRAIL LOGGING FUNCTION ---
def log_action(user, action, filename="N/A"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User: {user} | Action: {action} | File: {filename}\n"
    with open("audit_log.txt", "a") as log_file:
        log_file.write(log_entry)

# 1. login page rules
@app.route('/',methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in USERS and USERS[email] == password:
            session['user'] = email
            log_action(email, "LOGIN_SUCCESS")
            return redirect(url_for('dashboard'))
        else:
            log_action(email if email else "Unknown", "LOGIN_FAILED")
            return "Invalid Credentials. Try again.", 401
            
    return render_template('login.html')

# 2. access control
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dashboard.html', user=session['user'], files=files)

# 3. security file upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file", 400
            
        if file:
            filename = secure_filename(file.filename) # security
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #recore audit trail
            log_action(session['user'], "FILE_UPLOAD", filename)
            return redirect(url_for('dashboard'))
            
    return render_template('upload.html')

# 4. secure file download
@app.route('/view/<filename>')
def view_file(filename):
    if 'user' not in session:
        log_action("Anonymous", "UNAUTHORIZED_ACCESS_ATTEMPT", filename)
        return "Unauthorized Access", 403
        
    #in audit trail record download history 
    log_action(session['user'], "FILE_VIEW/DOWNLOAD", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 5. login route
@app.route('/logout')
def logout():
    user = session.get('user', 'Unknown')
    session.pop('user', None)
    log_action(user, "LOGOUT")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)