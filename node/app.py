from flask import Flask, request, jsonify
import requests, argparse, random, os, json, threading, time, socket

app = Flask(__name__)

# Cargar la configuración del nodo
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config
    
# Cargar la configuración
config = load_config()

# Obtener informacion de bootstrap
superpeer_host = config.get('superpeer_host', 'Internet-Facing-1575917799.us-east-1.elb.amazonaws.com')
superpeer_port = config.get('superpeer_port', 8080)
default_timeout = config.get('default_timeout', 10)
resources_path_config = config.get('resources_path', '../resources/resources.txt')
ping_interval = config.get('ping_interval', 5)

# Leer recursos desde el archivo
def load_resources(file_path, num_resources):
    with open(file_path, 'r') as file:
        all_resources = file.read().splitlines()
    return random.sample(all_resources, num_resources)

# Configurar argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='Iniciar un nodo con un nombre y recursos')
parser.add_argument('node_name', type=str, help='Nombre del nodo')
parser.add_argument('node_port', type=int, help='Puerto en el que se ejecutará el nodo')
args = parser.parse_args()

# Ruta del directorio de recursos
resources_path = os.path.join(os.path.dirname(__file__), resources_path_config)

# Simulando los recursos que tiene este nodo con 2 recursos por defecto por nodo
resources = load_resources(resources_path, 2)

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
        return jsonify({"message": f"File {file_name} uploaded successfully."}), 200
    except Exception as e:
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
        print(f"Error downloading file: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Función para actualizar el superpeer
def update_superpeer():
    try:
        data = {
            "node_id": args.node_name,
            "resources": resources
        }
        response = requests.post(f"http://{superpeer_host}:{superpeer_port}/register", json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error updating superpeer: {str(e)}")

# Función para registrar el nodo en el superpeer
def register_with_superpeer():
    try:
        superpeer_url = f"http://{superpeer_host}:{superpeer_port}/register"
        data = {
            "node_id": args.node_name,
            "resources": resources
        }
        response = requests.post(superpeer_url, json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error registering with superpeer: {str(e)}")

# Función para mantener la conexión con el superpeer
def keep_connection():
    while True:
        try:
            # Crear un socket tcp para mantener la conexión
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Establecer un timeout de 10 segundos
                sock.settimeout(default_timeout)
                # Intentar conectar al superpeer
                result = sock.connect_ex((superpeer_host, superpeer_port))
            if result != 0:
                print("Superpeer is not available")
                os._exit(1)
        except Exception as e:
            print(f"Error keeping connection: {str(e)}")
        time.sleep(ping_interval)

# Iniciar un hilo para mantener la conexión con el superpeer
ping_thread = threading.Thread(target=keep_connection, daemon=True)
ping_thread.start()

if __name__ == '__main__':
    register_with_superpeer()
    app.run(host='0.0.0.0', port=args.node_port)
