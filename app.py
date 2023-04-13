from flask import Flask, request, render_template, session, redirect, url_for
import yaml
import os
import sys
import secrets
import base64
import subprocess
import pwd

app = Flask(__name__)

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


#app.config['PORT'] = config['configuration']['port']
#app.config["SECRET_KEY"] = config['configuration']['secret_app']



def generate_secret():
    key = secrets.token_bytes(24)
    key_b64 = base64.b64encode(key).decode()
    key_b64 = key_b64.ljust(16, "=")
    return key_b64

########################################


########################################





@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if config['configuration']['install'] == 0:
        return redirect(url_for('install'))

    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # If user does not select file, browser also

        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'

        
        
        # If file is selected, save it
        file.save(config['configuration']['file_path']+"/"+file.filename)
        return 'File uploaded successfully'

    
    # Render the list_files.html template with the list of files
    return render_template('index.html')

@app.route('/list', methods=['GET', 'POST'])
def list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    path = config['configuration']['file_path']

    files = []
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root.replace(path,""),filename))



    return render_template('list_files.html', files=files)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if username and password are valid
        username = request.form['username']
        password = request.form['password']
        if username == config['login']['username'] and password == config['login']['password']:
            session['logged_in'] = True
            # Redirect to upload page if login is successful
            return redirect(url_for('upload_file'))
        else:
            # Display error message if login is unsuccessful
            return 'Invalid login'

        
    return render_template('login.html')





@app.route('/read/<filename>', methods=['GET'])
def read_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Check if file exists
    path = config['configuration']['file_path']
    file_path = os.path.join(path, filename)
    if not os.path.isfile(file_path):
        return 'File does not exist'


    # Read the contents of the file
    with open(file_path, 'r') as f:
        contents = f.read()

    

    # Render the read_file.html template with the contents of the file
    return render_template('read_file.html', filename=filename, contents=contents)





@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    path = config['configuration']['file_path']
    file_path = os.path.join(path, filename)
    with open(file_path, 'r') as file:
        file_contents = file.read()
    if request.method == 'POST':
        new_contents = request.form['new_contents']
        new_contents=new_contents.replace("\n","")
        with open(file_path, 'w') as file:
            file.write(new_contents)
        return redirect(url_for('read_file', filename=filename))
    return render_template('edit.html', filename=filename, contents=file_contents)









def get_home_dir():
    for entry in os.scandir('/home'):
        if entry.is_dir() and not entry.is_symlink():
            username = entry.name
            home_dir = pwd.getpwnam(username).pw_dir
            return home_dir
        
def linux():
    if sys.platform.startswith('linux'):
        import pwd
        return get_home_dir()+"/upload"

@app.route('/config', methods=['GET', 'POST'])
def install():
    if config['configuration']['install'] == 1:
        return redirect(url_for('upload_file'))
    else:
      if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        path = request.form['dir']
        port = request.form['port']
        config['configuration']['install'] = 1
        config['configuration']['port'] = int(port)
        config['login']['password'] = password 
        config['login']['username'] = username
        config['configuration']['secret_app']= generate_secret()
        config['configuration']['file_path'] = path
        subprocess.run(["mkdir", "-p", path])
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
        subprocess.run(['bash', "reload.sh"])
        return redirect(url_for('upload_file'))
      return render_template('config.html',config=config, dir=linux())
      




if __name__ == '__main__':
    app.config['PORT'] = config['configuration']['port']
    app.config["SECRET_KEY"] = config['configuration']['secret_app']
    app.config["HOST"] = config['configuration']['bind']
    app.run(host=app.config["HOST"],port=app.config['PORT'])
