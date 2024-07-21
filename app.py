from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Configuración de la conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['services']
collection = db['restaurant']

# Obtener todos los servicios de un usuario por su email
@app.route('/services/<email>', methods=['GET'])
def get_services_by_email(email):
    services = list(collection.find({"info.contact.email": email}))
    for service in services:
        service['_id'] = str(service['_id'])
    return jsonify(services), 200

# Insertar un nuevo elemento
@app.route('/service', methods=['POST'])
def add_service():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Obtener un elemento por su ID
@app.route('/service/<id>', methods=['GET'])
def get_service(id):
    service = collection.find_one({'_id': ObjectId(id)})
    if service:
        service['_id'] = str(service['_id'])
        return jsonify(service), 200
    else:
        return jsonify({'error': 'No se encontró el elemento'}), 404

# Editar un elemento existente
@app.route('/service/<id>', methods=['PUT'])
def update_service(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'error': 'No se encontró el elemento'}), 404
    return jsonify({'message': 'Elemento actualizado'}), 200

# Eliminar un elemento existente
@app.route('/service/<id>', methods=['DELETE'])
def delete_service(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'No se encontró el elemento'}), 404
    return jsonify({'message': 'Elemento eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)