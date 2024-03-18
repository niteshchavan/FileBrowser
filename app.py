from flask import Flask, render_template, request
import os
from datetime import datetime


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    folders = get_folders_list()
    organized_folders = organize_folders_by_date(folders)
    return render_template('index.html',  folders=organized_folders)

def get_folders_list():
    folders = []
    uploads_path = os.path.join(app.config['UPLOAD_FOLDER'])
    
    for root, dirs, files in os.walk(uploads_path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            print(folder_path)
            folders.append(folder_path)
            
    return folders


def organize_folders_by_date(folders):
    organized_folders = {}
    for folder in folders:
        date_folder = folder.split('/')[0]  # Extract date from folder name
        if date_folder not in organized_folders:
            organized_folders[date_folder] = []
        organized_folders[date_folder].append(folder)
    return organized_folders

def get_date_folder():
    current_date = datetime.now()
    date_folder = current_date.strftime("%Y-%m-%d")
    return date_folder
    
    
@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    folder_name = request.form['folderName']
    files = request.files.getlist('files')
    
    print("Folder Name:", folder_name)
    print("Files:")
    for file in files:
        print(file.filename)
    
    date_folder = get_date_folder()
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], date_folder, folder_name)
    print(folder_path)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
    
    for file in files:
        # Get relative path within the folder structure
        relative_path = os.path.relpath(file.filename, folder_name)
        file_path = os.path.join(folder_path, relative_path)
        
        # Create internal folders if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the file
        file.save(file_path)
    
    return "Folder uploaded successfully!"
    return "Folder uploaded successfully!"


if __name__ == '__main__':
    app.run(debug=True)
