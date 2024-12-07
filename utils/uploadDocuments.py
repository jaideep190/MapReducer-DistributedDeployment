import requests

def uploadFile(file_path, url, file_name):
    with open(file_path, 'rb') as file:
        files = {'file': (file_name, file, 'text/plain')}

        response = requests.post(url, files=files)

        return response

        