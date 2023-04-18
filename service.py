import crypt
import datetime
import os
import spwd
import subprocess


def check_user(username, password):
    # Check if the user exists
    try:
        spwd.getspnam(username)
    except KeyError:
        print(f"User {username} does not exist.")
        return False
    
    # Get the password hash from /etc/shadow
    hashed_pw = spwd.getspnam(username).sp_pwd
    # Extract the salt from the hashed password
    salt = hashed_pw.split('$')[2]
    # Encrypt the password with the same salt
    encrypted_pw = crypt.crypt(password, f'$6${salt}$')
    
    # print(f"{encrypted_pw} {hashed_pw}",flush=True)
    # Compare the encrypted passwords
    if encrypted_pw == hashed_pw:
        
        print(f"Password for user {username} is correct.",flush=True)
        return True
    else:
        print(f"Password for user {username} is incorrect.",flush=True)
        return False
   
def get_home_dir_data(username):
    home_dir = os.path.expanduser(f"~{username}")

    data = []
    dict = {}
    for filename in os.listdir(home_dir):
        filepath = os.path.join(home_dir, filename)
        stat = os.stat(filepath)
        file_data = {
            "name": filename,
            "time": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "size": stat.st_size,
            "path": filepath.replace('/','_')
        }
        data.append(file_data)

        if os.path.isdir(filepath):
            dict[filepath]=get_directory_data(filepath,dict)
    dict[home_dir]=data
    return dict

def get_directory_data(directory,dict):
    data = [{
            "name": "Parent_dir",
            "time": "",
            "size": "",
            "path": "Parent_dir"
        }]
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        stat = os.stat(filepath)
        file_data = {
            "name": filename,
            "time": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "size": stat.st_size,
            "path": filepath.replace('/','_')
        }
        data.append(file_data)

        if os.path.isdir(filepath):
            dict[filepath]=get_directory_data(filepath,dict)
    return data


def stats_path(path):
    num_files = 0
    num_dirs = 0
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        # Incrémente le nombre de répertoires
        num_dirs += len(dirnames)

        # Incrémente le nombre de fichiers et calcule leur taille totale
        for f in filenames:
            num_files += 1
            total_size += os.path.getsize(os.path.join(dirpath, f))

    # Convertit la taille totale en octets en gigaoctets
    total_size_kb = round(total_size / 1024, 2)
    return {'total_size': total_size_kb.__str__()+' Kb','num_files': num_files,'num_dirs': num_dirs}


def search_directory(start_path, name):
    matches = []
    for root, dirnames, filenames in os.walk(start_path):
        for dirname in dirnames:
            if dirname.startswith(name):
                path = os.path.join(root, dirname)
                stat = os.stat(path)
                matches.append({
                    "name": dirname,
                    "time": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    "size": stat.st_size,
                    "path": path.replace('/','_')
                })
        for filename in filenames:
            if filename.startswith(name):
                path = os.path.join(root, filename)
                stat = os.stat(path)
                matches.append({
                    "name": filename,
                    "time": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    "size": stat.st_size,
                    "path": path.replace('/','_')
                })
    return matches

def search_extension(start_path, ext):
    matches = []
    for root, dirnames, filenames in os.walk(start_path):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            if file_extension.startswith(ext):
                path = os.path.join(root, filename)
                stat = os.stat(path)
                matches.append({
                    "name": filename,
                    "time": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    "size": stat.st_size,
                    "path": path.replace('/','_')
                })
    return matches