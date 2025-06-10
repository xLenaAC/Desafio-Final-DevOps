# test_app.py
import pytest
from app import app # Importa a instância 'app' do seu arquivo app.py

@pytest.fixture
def client():
    """Configura o cliente de teste do Flask para cada função de teste."""
    app.config['TESTING'] = True
    # Para testes com JWT, é bom garantir que a chave secreta seja consistente
    # Se ela já está em app.config['JWT_SECRET_KEY'], não precisa redefinir aqui
    # app.config['JWT_SECRET_KEY'] = 'test-secret-key' # Pode ser diferente da produção
    with app.test_client() as client:
        yield client

def test_home(client):
    """Testa a rota principal '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API is running"}

def test_get_items(client):
    """Testa a rota '/items'."""
    response = client.get('/items')
    assert response.status_code == 200
    assert response.get_json() == {"items": ["item1", "item2", "item3"]}

def test_login_returns_token(client):
    """Testa se a rota '/login' retorna um token de acesso."""
    response = client.post('/login') # Não precisa enviar dados para este endpoint de login específico
    assert response.status_code == 200
    json_data = response.get_json()
    assert "access_token" in json_data
    assert isinstance(json_data["access_token"], str)
    assert len(json_data["access_token"]) > 0

def test_protected_route_without_token(client):
    """Testa a rota protegida sem um token JWT, esperando 401."""
    response = client.get('/protected')
    assert response.status_code == 401
    json_data = response.get_json()
    assert "msg" in json_data
    # A mensagem exata pode variar dependendo da configuração do Flask-JWT-Extended
    # "Missing Authorization Header" é comum.
    assert "Missing Authorization Header" in json_data["msg"] or "Authorization Required" in json_data["msg"]


def test_protected_route_with_valid_token(client):
    """Testa a rota protegida com um token JWT válido."""
    # 1. Fazer login para obter um token
    login_response = client.post('/login')
    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    # 2. Usar o token para acessar a rota protegida
    headers = {
        'Authorization': f'Bearer {token}'
    }
    protected_response = client.get('/protected', headers=headers)
    assert protected_response.status_code == 200
    assert protected_response.get_json() == {"message": "Protected route"}

def test_protected_route_with_invalid_token(client):
    """Testa a rota protegida com um token JWT inválido."""
    headers = {
        'Authorization': 'Bearer invalidtoken123'
    }
    response = client.get('/protected', headers=headers)
    assert response.status_code == 422 # Flask-JWT-Extended geralmente retorna 422 para token malformado/inválido
    json_data = response.get_json()
    assert "msg" in json_data
    # Exemplos de mensagens de erro para token inválido:
    assert "Invalid token" in json_data["msg"] or "Not enough segments" in json_data["msg"] or "Token is invalid" in json_data["msg"]



# Opcional: Testar se a rota do documento Swagger (se você o tiver estaticamente) responde
# Se você não tiver /static/swagger.json, este teste falhará com 404.
# def test_swagger_api_doc_route(client):
#     """Testa se a rota para o swagger.json (se existir estaticamente) está acessível."""
#     response = client.get('/static/swagger.json')
#     # Se o arquivo existir, deve ser 200. Se não, 404.
#     # Para este exemplo, vamos assumir que você pode não tê-lo ainda.
#     assert response.status_code == 200 or response.status_code == 404

def test_swagger_api_doc_route(client):
    """Testa se a rota para o swagger.json está acessível."""
    response = client.get('/static/swagger.json') # Ajuste o caminho se for diferente
    assert response.status_code == 200
    assert response.is_json # Verifica se o content-type é json
    json_data = response.get_json()
    assert "swagger" in json_data # Verifica um campo chave do swagger.json
    assert json_data["info"]["title"] == "InovaTech API"
