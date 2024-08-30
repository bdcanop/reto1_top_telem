from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

nodes = {}
superpeers = []

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
superpeers.extend(known_superpeers)

# Obtener host y puerto del superpeer
host = config.get('host', '0.0.0.0')
port = config.get('port', 8080)

# Endpoint para registrar un nodo
@app.route('/register', methods=['POST'])
def register_node():
    try:
        data = request.json
        node_id = data['node_id']
        resources = data['resources']
        nodes[node_id] = resources

        print(f"Node {node_id} registered, nodes: {nodes}. #: {len(nodes)}")

        return jsonify({"message": f"Node {node_id} registered successfully. Total nodes: {len(nodes)}"})
    except Exception as e:
        print(f"Error registering node: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para registrar un superpeer
@app.route('/register-superpeer', methods=['POST'])
def register_superpeer():
    try:
        data = request.json
        superpeer_address = data['address']
        if superpeer_address not in superpeers:
            superpeers.append(superpeer_address)
            print(f"Superpeer {superpeer_address} registered. Total superpeers: {len(superpeers)}")
        return jsonify({"message": f"Superpeer {superpeer_address} registered successfully. Total superpeers: {len(superpeers)}"})
    except Exception as e:
        print(f"Error registering superpeer: {str(e)}")
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
        for superpeer in superpeers:
            try:
                response = requests.get(f"http://{superpeer}/search", params={"resource": resource_name})
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error searching resource in superpeer {superpeer}: {str(e)}")
        
        return jsonify({"Message": "Resource not found"}), 404
    except Exception as e:
        print(f"Error searching resource: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para listar todos los nodos y los recursos disponibles
@app.route('/list-resources', methods=['GET'])
def list_nodes_and_resources():
    try:
        return jsonify(nodes)
    except Exception as e:
        print(f"Error listing nodes: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para listar todos los superpeers registrados
@app.route('/list-superpeers', methods=['GET'])
def list_superpeers():
    try:
        return jsonify(superpeers)
    except Exception as e:
        print(f"Error listing superpeers: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def home():
    return "<h1>Welcome to the Peer Connection Server</h1><p>This server is currently handling peer connections.</p>"

if __name__ == '__main__':
    app.run(host=host, port=port)