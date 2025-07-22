"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)

    return jsonify({
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_single_member(id):

    deleted = jackson_family.delete_member(id)

    if deleted:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 400


@app.route('/members', methods=['POST'])
def create_member():

    # agregar el miembro a la familia
    # agregar un nuevo elemento a la familia
    # leer los datos del body
    body = request.json
    # utilizar el metodo add_member
    member = {'first_name':body['first_name'] ,'age':body['age'], 'lucky_numbers':body['lucky_numbers']}
    new_member = jackson_family.add_member(member)

    # This is how you can use the Family datastructure by calling its methods
    return jsonify(new_member), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
