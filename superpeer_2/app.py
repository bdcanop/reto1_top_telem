from flask import Flask, request, jsonify
import requests, os, json, threading, time, logging

app = Flask(__name__)

nodes = {} # Nodos registrados en el superpeer
known_superpeers = [] # Lista de superpeers conocidos
active_superpeers = [] # Lista de superpeers activos

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler("superpeer2.log"),
        logging.StreamHandler()
    ]
)

# Cargar la configuración del super peer
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config
    
# Cargar la configuración
config = load_config()

# Registrar los superpeers conocidos al iniciar la aplicación
known_superpeers = config.get('known_superpeers', [])
active_superpeers.extend(known_superpeers)

# Obtener host y puerto del superpeer
superpeer_host = config.get('host', '0.0.0.0')
superpeer_port = config.get('port', 8080)
default_timeout = config.get('default_timeout', 2)

# Función para verificar la disponibilidad de los superpeers
def ping_superpeers():
    while True:
        for superpeer in known_superpeers[:]: # Esto es una copia de la lista
            try:
                response = requests.get(f"http://{superpeer}/health") # Endpoint de salud de los superpeers
                if response.status_code == 200 and superpeer not in active_superpeers:
                    active_superpeers.append(superpeer)
                    logging.info(f"Superpeer {superpeer} is back online and added to the network")
            except requests.exceptions.RequestException:
                if superpeer in active_superpeers:
                    active_superpeers.remove(superpeer)
                    logging.info(f"Superpeer {superpeer} is offline and removed from the network")
        time.sleep(default_timeout) # Espera 2 segundos antes de volver a verificar

# Iniciar el hilo para verificar la disponibilidad de los superpeers
ping_thread = threading.Thread(target=ping_superpeers, daemon=True)
ping_thread.start()

# Endpoint de salud para verificar la disponibilidad del superpeer
@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy", 200

# Endpoint para registrar un nodo
@app.route('/register', methods=['POST'])
def register_node():
    try:
        data = request.json
        node_id = data['node_id']
        resources = data['resources']
        nodes[node_id] = resources

        logging.info(f"Node {node_id} registered, nodes: {nodes}. #: {len(nodes)}")
        return jsonify({"message": f"Node {node_id} registered successfully. Total nodes: {len(nodes)}"}), 200
    
    except Exception as e:
        logging.error(f"Error registering node: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para buscar recursos
@app.route('/search', methods=['GET'])
def search():
    try:
        resource_name = request.args.get('resource')

        if not resource_name:
            return jsonify({"error": "Resource parameter is required"}), 400
        
        # Buscar en los nodos locales
        for node_id, resources in nodes.items():
            if resource_name in resources:
                return jsonify({"node_id": node_id, "resource": resource_name})
        
        # Si no se encuentra localmente, buscar en otros superpeers
        for superpeer in active_superpeers:
            try:
                response = requests.get(f"http://{superpeer}/search", params={"resource": resource_name})
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logging.warning(f"Error searching resource in superpeer {superpeer}: {str(e)}")
        return jsonify({"message": "Resource not found"}), 404
    
    except Exception as e:
        logging.error(f"Error searching resource: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para listar todos los nodos y los recursos disponibles
@app.route('/list-resources', methods=['GET'])
def list_nodes_and_resources():
    try:
        return jsonify(nodes)
    except Exception as e:
        logging.error(f"Error listing nodes: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para listar todos los superpeers registrados
@app.route('/list-superpeers', methods=['GET'])
def list_superpeers():
    try:
        return jsonify(active_superpeers)
    except Exception as e:
        logging.error(f"Error listing superpeers: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def home():
    return "<h1>Welcome to the Peer Connection Server</h1><p>This server is currently handling peer connections.</p>"

if __name__ == '__main__':
    app.run(host=superpeer_host, port=superpeer_port)