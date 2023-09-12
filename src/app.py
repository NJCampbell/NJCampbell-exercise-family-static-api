"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object is initializing dict (adding a list of dictionaries inside)
jackson_family = FamilyStructure("Jackson")

# create dictionaries (object) to add to the jackson family list (array)
# python list of dictionaries = js an array of objects
# create 3 dicts of family members in instructions


jackson_family.add_member({
    'first_name': 'John', 'last_name': 'Jackson', 'age': 33, 'lucky_numbers': [7, 13, 22]
})
jackson_family.add_member({
    'first_name': 'Jane', 'last_name': 'Jackson', 'age': 35, 'lucky_numbers': [10, 14, 3]
})
jackson_family.add_member({
    'first_name': 'Jimmy', 'last_name': 'Jackson', 'age': 5, 'lucky_numbers': [1]
})   







# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_family_members():

    # this is how you can use the Family datastructure by calling its methods (line 16 is jackson family)
    members = jackson_family.get_all_members()
    return jsonify(members), 200


    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_a_single_member(member_id):
    member = jackson_family.get_member(member_id)
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def create_new_member():
    # receive some json object of a family member
    member = request.json
    # {first_name, last_name, age, lucky_numbers}
    # call add_member function to append this new family member to the list
    jackson_family.add_member(member)
    # return some statement or string with a 200 
    return f"You successfully add a {member['first_name']} {member['last_name']} to the list.", 200
    

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_a_single_member(member_id):
    pass


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
