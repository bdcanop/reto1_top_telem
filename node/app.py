from flask import Flask, request, jsonify
import requests, argparse, random, os

app = Flask(__name__)

# Configuracion de logging
# logging.basicConfig(level=logging.INFO)

# Leer recursos desde el archivo
def load_resources(file_path, num_resources):
    with open(file_path, 'r') as file:
        all_resources = file.read().splitlines()
    return random.sample(all_resources, num_resources)

# Configurar argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='Iniciar un nodo con un nombre y una cantidad de archivos a compartir.')
parser.add_argument('node_name', type=str, help='Nombre del nodo')
parser.add_argument('num_files', type=int, help='Cantidad de archivos a compartir')
parser.add_argument('port', type=int, help='Puerto en el que se ejecutará el nodo')
args = parser.parse_args()

# Ruta del directorio de recursos
resources_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'resources.txt')

# Simulando los recursos que tiene este nodo
resources = load_resources(resources_path, args.num_files)

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
        #logging.error(f"Error uploading file: {str(e)}")
        print(f"Error uploading file: {str(e)}")
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
        #logging.error(f"Error downloading file: {str(e)}")
        print(f"Error downloading file: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Función para actualizar el superpeer
def update_superpeer():
    try:
        #logging.info("====| UPDATING SUPER PEER |====")
        print("====| UPDATING SUPER PEER |====")
        data = {
            "node_id": args.node_name,
            "resources": resources
        }
        response = requests.post("http://3.228.32.5:8080/register", json=data)
        response.raise_for_status()
        #logging.info(response.json())
        print(response.json())
    except requests.exceptions.RequestException as e:
        #logging.error(f"Error updating superpeer: {str(e)}")
        print(f"Error updating superpeer: {str(e)}")


# Función para registrar el nodo en el superpeer
def register_with_superpeer():
    try:
        superpeer_url = "http://3.228.32.5:8080/register"
        data = {
            "node_id": args.node_name,
            "resources": resources
        }
        response = requests.post(superpeer_url, json=data)
        response.raise_for_status()
        #logging.info(response.json())
        print(response.json())
    except requests.exceptions.RequestException as e:
        #logging.error(f"Error registering with superpeer: {str(e)}")
        print(f"Error registering with superpeer: {str(e)}")

if __name__ == '__main__':
    register_with_superpeer()
    app.run(host='0.0.0.0', port=args.port)
