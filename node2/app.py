from flask import Flask, request, jsonify
import requests, logging

app = Flask(__name__)

# Configuracion de logging
logging.basicConfig(level=logging.INFO)

# Simulando los recursos que tiene este nodo
resources = ["file3.txt", "file4.txt"]

# Endpoint para subir un archivo dummy
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        if not data or 'file_name' not in data:
            return jsonify({"error": "Invalid input"}), 400
        
        file_name = request.json['file_name']
        resources.append(file_name)
        update_superpeer()
        return jsonify({"message": f"File {file_name} uploaded successfully."})
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para descargar un archivo dummy
@app.route('/download', methods=['GET'])
def download():
    try:
        file_name = request.args.get('file_name')
        if not file_name:
            return jsonify({"error": "File name parameter is required"}), 400
        
        if file_name in resources:
            return jsonify({"message": f"Downloading {file_name}..."}), 200
        return jsonify({"message": "File not found"}), 404
    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Función para actualizar el superpeer
def update_superpeer():
    try:
        logging.info("====| UPDATING |====")
        data = {
            "node_id": "Node2",
            "resources": resources
        }
        response = requests.post("http://localhost:8080/register", json=data)
        response.raise_for_status()
        logging.info(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating superpeer: {str(e)}")


# Función para registrar el nodo en el superpeer
def register_with_superpeer():
    try:
        superpeer_url = "http://localhost:8080/register"
        data = {
            "node_id": "Node2",
            "resources": resources
        }
        response = requests.post(superpeer_url, json=data)
        response.raise_for_status()
        logging.info(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error registering with superpeer: {str(e)}")

if __name__ == '__main__':
    register_with_superpeer()
    app.run(host='0.0.0.0', port=8082)
