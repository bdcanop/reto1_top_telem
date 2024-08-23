from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Simulando los recursos que tiene este nodo
resources = ["file3.txt", "file4.txt"]

# Endpoint para subir un archivo (dummy)
@app.route('/upload', methods=['POST'])
def upload():
    file_name = request.json['file_name']
    resources.append(file_name)
    update_superpeer()
    return jsonify({"message": f"File {file_name} uploaded successfully."})

# Endpoint para descargar un archivo (dummy)
@app.route('/download', methods=['GET'])
def download():
    file_name = request.args.get('file_name')
    if file_name in resources:
        return jsonify({"message": f"Downloading {file_name}..."}), 200
    return jsonify({"message": "File not found"}), 404

def update_superpeer():
    print("UPDATING")
    data = {
        "node_id": "Node2",
        "resources": resources
    }
    response = requests.post("http://localhost:5000/register", json=data)
    print(response.json())

# Función para registrar el nodo en el superpeer
def register_with_superpeer():
    superpeer_url = "http://localhost:5000/register"
    data = {
        "node_id": "Node2",
        "resources": resources
    }
    response = requests.post(superpeer_url, json=data)
    print(response.json())

if __name__ == '__main__':
    register_with_superpeer()
    app.run(host='0.0.0.0', port=5002)
