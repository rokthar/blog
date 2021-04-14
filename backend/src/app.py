from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/heroes"
CORS(app)
mongo = PyMongo(app)

# RUTAS
@app.route('/users', methods=['POST'])
def create_user():
    #reciviendo datos
    username = request.json['username']
    usermail = request.json['mail']
    userpass = request.json['pass']

    if username and usermail and userpass:
        hased_pass = generate_password_hash(userpass)
        id = mongo.db.users.insert(
            {
                'username':username,
                'mail':usermail,
                'pass':hased_pass
            } 
        )
        response = {
                'id': str(id),
                'username':username,
                'mail':usermail,
                'pass':hased_pass
            }
        return response
    else:
        return not_found()
        #return {'mensaje':'Datos Faltantes'}

@app.route('/users', methods=['GET'])
def get_users():
    users_list = mongo.db.users.find()
    response = json_util.dumps(users_list)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user_byid(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'mensaje':'the user has been eliminate'
    })
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    usermail = request.json['mail']
    userpass = request.json['pass']
    if(username and usermail and userpass):
        hash_pass = generate_password_hash(userpass)
        mongo.db.users.update_one({'_id':ObjectId(id)}, {'$set': {
            'username':usermail,
            'mail':usermail,
            'pass':hash_pass
        }})
    
    response = jsonify({
        'mensaje':'the user has been actualizate successfuly'
    })
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado: '+ request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)