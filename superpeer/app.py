from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar la información de los nodos y sus recursos
nodes = {}

# Endpoint para que los nodos se registren
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    node_id = data['node_id']
    resources = data['resources']
    nodes[node_id] = resources
    with open('registros.txt', 'w') as archivo:
        archivo.write(f"{node_id} registered, nodes: {nodes}. #: {len(nodes)}")
    return jsonify({"message": f"Node {node_id} registered successfully. number of nodes: {nodes} {len(nodes)}"})

# Endpoint para buscar recursos
@app.route('/search', methods=['GET'])
def search():
    resource_name = request.args.get('resource')
    for node_id, resources in nodes.items():
        if resource_name in resources:
            return jsonify({"node_id": node_id, "resource": resource_name})
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
