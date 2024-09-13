""" 
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from api.utils import APIException, generate_sitemap
from api.models import db  # Aquí se importa db desde models.py, donde está SQLAlchemy
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos y Flask-Migrate
db.init_app(app)  # Inicialización de SQLAlchemy
migrate = Migrate(app, db)  # Migraciones de la base de datos

# Configuración de JWT y Bcrypt
app.config["JWT_SECRET_KEY"] = "wert7410"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Habilitar CORS
CORS(app)

# Define si estás en desarrollo o producción
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
app.url_map.strict_slashes = False

# Añadir administración y comandos personalizados
setup_admin(app)
setup_commands(app)

# Registrar rutas del API (importamos las rutas desde routes.py)
from api.routes import api
app.register_blueprint(api, url_prefix='/api')

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar el sitemap con todos los endpoints
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# Cualquier otra ruta tratará de servir un archivo estático
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # Evitar caché
    return response

# Ejecuta la aplicación en el puerto especificado
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
