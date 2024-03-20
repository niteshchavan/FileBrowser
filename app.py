from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import os
from datetime import datetime

app = Flask(__name__)

ALLOWED_DIRECTORY = 'Data'

@app.route('/')
def index():
    # Get the directory path from the query parameter
    directory = request.args.get('dir', '')

    # Get the list of files and directories in the specified directory
    full_directory_path = os.path.join(ALLOWED_DIRECTORY, directory)
    contents = os.listdir(full_directory_path)

    # Render the template with the list of contents and current directory
    return render_template('index.html', contents=contents, current_directory=directory)

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    folder_name = request.form['folderName']
    files = request.files.getlist('files')
    
    print("Folder Name:", folder_name)
    print("Files:")
    for file in files:
        print(file.filename)
    
    date_folder = get_date_folder()
    folder_path = os.path.join(ALLOWED_DIRECTORY, date_folder, folder_name)
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

def get_date_folder():
    current_date = datetime.now()
    date_folder = current_date.strftime("%Y-%m-%d")
    return date_folder


@app.route('/navigate')
def navigate_directory():
    # Get the current directory from the query parameter
    current_directory = request.args.get('dir', '')

    # Get the target directory from the clicked link
    target_directory = request.args.get('target')

    # Construct the new directory path
    if target_directory == '..':
        # If the target directory is '..', go up one level
        new_directory = os.path.dirname(current_directory)
    else:
        # Otherwise, navigate to the selected directory
        new_directory = os.path.join(current_directory, target_directory)

    # Redirect to the root URL with the new directory as a query parameter
    return redirect(url_for('index', dir=new_directory))
    
@app.before_request
def check_directory_access():
    # Get the requested directory from the query parameter
    requested_directory = request.args.get('dir', '')

    # Construct the full path of the requested directory
    full_requested_path = os.path.join(ALLOWED_DIRECTORY, requested_directory)

    # Check if the requested directory is within the allowed directory
    if not os.path.abspath(full_requested_path).startswith(os.path.abspath(ALLOWED_DIRECTORY)):
        # If not, abort the request with a 403 Forbidden status code
        abort(403)


@app.route('/upload_selected_folders', methods=['POST'])
def upload_selected_folders():
    data = request.json  # Get the JSON data sent from the client
    selected_folders = data.get('folders', [])  # Get the list of selected folders
    selected_files = data.get('files', [])  # Get the list of selected files

    # Process the selected folders and files as needed
    print("Selected folders:", selected_folders)
    print("Selected files:", selected_files)

    # Return a JSON response indicating success
    return jsonify(message="Selected folders and files received successfully!")


        
if __name__ == '__main__':
    app.run(debug=True)
