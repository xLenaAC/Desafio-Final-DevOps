from flask import Flask, jsonify, send_from_directory # Adicionado send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os # Adicionado para path do static

app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_super_secret_dev_key') # Melhor usar env var
jwt = JWTManager(app)

### Swagger UI ###
SWAGGER_URL = '/swagger'
# API_DOC_URL agora aponta para uma rota que serve o swagger.json
API_DOC_URL_PATH = '/static/swagger.json' # O caminho real do arquivo
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_DOC_URL_PATH, # A URL que a UI do Swagger usará para buscar o JSON
    config={ # Opcional: configurações da UI
        'app_name': "InovaTech API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Rota para servir o swagger.json estático
# Isso é necessário porque API_DOC_URL aponta para este endpoint.
@app.route('/static/<path:filename>')
def serve_static(filename):
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_folder, filename)

@app.route('/')
def home():
    return jsonify(message="API is running")

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items=["item1", "item2", "item3"])

@app.route('/login', methods=['POST'])
def login():
    # Em uma aplicação real, você validaria credenciais aqui
    access_token = create_access_token(identity="test_user") # 'user' é um bom placeholder
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="Protected route")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1313, debug=True) # Adicionado debug=True para desenvolvimento
