from flask import Blueprint, request, jsonify
from api.models import db, User
from api.utils import APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from datetime import timedelta

api = Blueprint('api', __name__)
bcrypt = Bcrypt()

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def handle_signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    try:
        # Hashear la contraseña y crear un nuevo usuario
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            email=email,
            password=password_hash,
            is_active=True
        ) 
        db.session.add(new_user)
        db.session.commit()

        # Generar el token JWT con expiración opcional
        jwt_token = create_access_token(identity=new_user.id, expires_delta=timedelta(hours=1))
        
        return jsonify({"token": jwt_token}), 201  # Código 201 (Creado)

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500  # Cambia a un mensaje genérico en producción
        

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Buscar al usuario por email
    user = User.query.filter_by(email=email).first()

    # Verificar si el usuario existe y si la contraseña es correcta
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
