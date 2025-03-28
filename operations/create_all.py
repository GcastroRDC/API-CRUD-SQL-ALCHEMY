from operations.connector_database import db
from flask import jsonify
from app import app
from models.Usuarios import Usuarios

# O contexto de aplicação:
def createTable():

    with app.app_context():

        try:

            with app.app_context():

                db.create_all()

            return jsonify({"message": "Tabela criada com sucesso!"}), 200
        
        except Exception as e:

            return jsonify({"error": f"Erro ao criar a tabela: {e}"}), 500
        
