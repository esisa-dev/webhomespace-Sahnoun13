import hashlib
import logging
import os
from zipfile import ZipFile
import service
from flask import Flask, redirect, render_template, request, send_file, session, url_for

app = Flask(__name__)

def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()
app.secret_key='1234'

# to exclude the info logs
app.logger.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', handlers=[
        logging.FileHandler('logFile.log'),
        logging.StreamHandler()
    ])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    pwd=request.form['password']
  
    if service.check_user(username,pwd):
        app.secret_key=generate_key(username)
        session['data'] = service.get_home_dir_data(username)
        
        # print(data,flush=True)

        session['home_dir'] = "/home/" + username

        response=app.make_response(render_template('homepage.html',data=session['data']["/home/"+username]))
        session['user_id']=username
        
        logging.warning(f'{username} logged in')
        return response
    else:
        return render_template('index.html',error_auth='username or password incorrect')

@app.route('/logout')
def logout():
    username = session['user_id']
    logging.warning(f'{username} logged out')
    session.pop('user_id',None)
    session['data'] = {}
    session['home_dir'] = "/home/"
    return redirect(url_for('index'))

@app.route('/navig/<path>')
def navig(path):
    if 'user_id' in session :
        data = session['data']
        if path == "Parent_dir":
            session['home_dir']=os.path.dirname(session['home_dir'])
            return render_template('homepage.html',data=data[session['home_dir']])
        elif os.path.isdir(path.replace('_','/')):
            session['home_dir']=path.replace('_','/')
            return render_template('homepage.html',data=data[session['home_dir']])
        elif os.path.isfile(path.replace('_','/')):
            with open(path.replace('_','/'), 'r') as f:
                file_contents = f.read()
            return '<pre>' + file_contents + '</pre>'
        else :
            return render_template('homepage.html',data=data[session['home_dir']])

    else :
        return redirect('/')

@app.route('/search')
def search():
    if 'user_id' in session :
        query = request.args.get('query')
        data = session['data']
        if query is not None and query.startswith('.')==False:
            list = service.search_directory(session['home_dir'],query)
            return render_template('homepage.html',data=list)
        elif query is not None and query.startswith('.'):
            list = service.search_extension(session['home_dir'],query)
            return render_template('homepage.html',data=list)
        else :
            return render_template('homepage.html',data=data[session['home_dir']])

    else :
        return redirect('/')
    
@app.route('/files')
def files():
    if 'user_id' in session :
        dic = service.stats_path(session['home_dir'])
        data = session['data']
        data[session['home_dir']].append({
            "name": "Number of files",
            "time": "",
            "size": dic["num_files"]
        })
        return render_template('homepage.html',data=data[session['home_dir']])

    else :
        return redirect('/')
    
@app.route('/dirs')
def dirs():
    if 'user_id' in session :
        dic = service.stats_path(session['home_dir'])
        data = session['data']
        data[session['home_dir']].append({
            "name": "Number of Directories",
            "time": "",
            "size": dic["num_dirs"]
        })
        return render_template('homepage.html',data=data[session['home_dir']])

    else :
        return redirect('/')    

@app.route('/space')
def space():
    if 'user_id' in session :
        dic = service.stats_path(session['home_dir'])
        data = session['data']
        data[session['home_dir']].append({
            "name": "Space occupied",
            "time": "",
            "size": dic["total_size"]
        })
        return render_template('homepage.html',data=data[session['home_dir']])

    else :
        return redirect('/')

@app.route('/download')
def download():
    if 'user_id' in session :
        # Créer un objet ZipFile
        with ZipFile(session['user_id']+'.zip', 'w') as zip:
            # Ajouter tous les fichiers du répertoire au zip
            for root, dirs, files in os.walk('/home/'+session['user_id']):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip.write(file_path, os.path.relpath(file_path, '/home/'+session['user_id']))
        # Renvoyer le répertoire compressé
        username = session['user_id']
        logging.warning(f'{username} downloaded his home directory')
        return send_file(session['user_id']+'.zip', as_attachment=True)

    else :
        return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)