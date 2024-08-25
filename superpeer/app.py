from flask import Flask, request, jsonify
# import logging

app = Flask(__name__)

# Configuracion de logging
#logging.basicConfig(filename='registros.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Lista para almacenar la información de los nodos y sus recursos
nodes = {}

# Endpoint para que los nodos se registren
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data or 'node_id' not in data or 'resources' not in data:
            return jsonify({"Error": "Invalid input"}), 400
        
        node_id = data['node_id']
        resources = data['resources']
        nodes[node_id] = resources

        # logging.info(f"Node {node_id} registered, nodes: {nodes}. #: {len(nodes)}")
        print(f"Node {node_id} registered, nodes: {nodes}. #: {len(nodes)}")

        return jsonify({"message": f"Node {node_id} registered successfully. Total nodes: {len(nodes)}"})
    except Exception as e:
        #logging.error(f"Error registering node: {str(e)}")
        print(f"Error registering node: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint para buscar recursos
@app.route('/search', methods=['GET'])
def search():
    try:
        resource_name = request.args.get('resource')
        if not resource_name:
            return jsonify({"error": "Resource parameter is required"}), 400
        
        for node_id, resources in nodes.items():
            if resource_name in resources:
                return jsonify({"node_id": node_id, "resource": resource_name})
            
        return jsonify({"Message": "Resource not found"}), 404
    except Exception as e:
        #logging.error(f"Error searching resource: {str(e)}")
        print(f"Error searching resource: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    
# Endpoint para listar todos los nodos y los recursos disponibles
@app.route('/list', methods=['GET'])
def list_nodes_and_resources():
    try:
        return jsonify(nodes)
    except Exception as e:
        #logging.error(f"Error listing nodes: {str(e)}")
        print(f"Error listing nodes: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route('/')
def home():
    return "<h1>Welcome to the Peer Connection Server</h1><p>This server is currently handling peer connections.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
