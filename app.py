"""
API de exemplo completamente reescrita.

Principais diferenças em relação à versão anterior:
  • Usa Blueprint para isolar rotas
  • Persiste usuários em um dicionário (id → User)
  • Usa dataclasses para modelar entidade
  • Endpoints foram renomeados para /users
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import count
from typing import Dict

from flask import Blueprint, Flask, jsonify, request

# --------------------------------------------------------------------- #
# MODELO
# --------------------------------------------------------------------- #
@dataclass
class User:
    id: int
    name: str
    age: int


_db: Dict[int, User] = {}
_id_seq = count(start=1)

# --------------------------------------------------------------------- #
# BLUEPRINT
# --------------------------------------------------------------------- #
bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def list_users():
    """
    GET /users/  → lista todos os usuários
    """
    return jsonify([asdict(u) for u in _db.values()]), 200


@bp.route("/", methods=["POST"])
def create_user():
    """
    POST /users/  → cria novo usuário
    payload esperado: { "name": str, "age": int }
    """
    payload = request.get_json(silent=True) or {}
    if not {"name", "age"} <= payload.keys():
        return jsonify({"error": "invalid payload"}), 400

    uid = next(_id_seq)
    user = User(id=uid, name=payload["name"], age=payload["age"])
    _db[uid] = user
    return jsonify(asdict(user)), 201


@bp.route("/<int:uid>", methods=["GET"])
def retrieve_user(uid: int):
    """
    GET /users/<id>  → recupera usuário pelo id
    """
    if uid in _db:
        return jsonify(asdict(_db[uid])), 200
    return jsonify({"error": "user not found"}), 404


# --------------------------------------------------------------------- #
# APP FACTORY
# --------------------------------------------------------------------- #
def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(bp)

    @app.route("/")
    def healthcheck():
        """
        Health-check root.
        """
        return jsonify({"status": "ok"}), 200

    return app


# Instância global usada por gunicorn, testes, etc.
app = create_app()

# Execução local: `python app.py`
if __name__ == "__main__":
    app.run(debug=True, port=5000)
