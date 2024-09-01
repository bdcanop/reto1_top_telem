from flask import Flask, request, jsonify
import requests, argparse, random, os, threading, time, socket

app = Flask(__name__)

# Configuracion de logging
# logging.basicConfig(level=logging.INFO)

host_p = "127.0.0.1"

# Leer recursos desde el archivo
def load_resources(file_path, num_resources):
    with open(file_path, 'r') as file:
        all_resources = file.read().splitlines()
    return random.sample(all_resources, num_resources)

# Configurar argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='Iniciar un nodo con un nombre y una cantidad de archivos a compartir.')
parser.add_argument('node_name', type=str, help='Nombre del nodo')
parser.add_argument('num_files', type=int, help='Cantidad de archivos a compartir')
parser.add_argument('host', type=str, help='Host al que se conectara el super peer')
parser.add_argument('port', type=int, help='Puerto en el que se ejecutará el nodo')
# parser.add_argument('host_sp', type=str, help='Host del superpeer al que se conectará')
parser.add_argument('port_sp', type=int, help='Puerto del superpeer al que se conectará')

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
    
# Endpoint para probar
@app.route('/prueba', methods=['GET'])
def prueba():
    return jsonify({"message": f"{resources}uploaded successfully."})


# Función para actualizar el superpeer
def update_superpeer():
    try:
        #logging.info("====| UPDATING SUPER PEER |====")
        print("====| UPDATING SUPER PEER |====")
        data = {
            "node_id": args.node_name,
            "resources": resources
        }
        #response = requests.post("http://3.228.32.5:8080/register", json=data)
        response = requests.post(f"http://{host_p}:{args.port_sp}/register", json=data)
        response.raise_for_status()
        #logging.info(response.json())
        print(response.json())
    except requests.exceptions.RequestException as e:
        #logging.error(f"Error updating superpeer: {str(e)}")
        print(f"Error updating superpeer: {str(e)}")


# Función para registrar el nodo en el superpeer
def register_with_superpeer():
    try:
        superpeer_url = f"http://{host_p}:{args.port_sp}/register"
        print(f"esta es la url: {superpeer_url}")
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

def ping_superpeers():
    while(True):
        try:
        # Crear un socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Establecer un timeout de 3 segundos
                sock.settimeout(3)
                # Intentar conectar al servidor en el puerto especificado
                result = sock.connect_ex((host_p, int(args.port_sp)))
            if result != 0:
                print("The server is not available")
                os._exit(1)
        except Exception as e:
            print(f"An error ocurred while ping \n {e}")
        time.sleep(5)

ping_thread = threading.Thread(target=ping_superpeers, daemon=True)
ping_thread.start()

if __name__ == '__main__':
    register_with_superpeer()
    app.run(host=args.host, port=args.port)
