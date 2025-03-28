from flask import Flask, Response, request
from models.Usuarios import Usuarios
from handles.handle_response import handle_response
from operations.connector_database import db  # Importando a instância db
import mysql.connector


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost:3306/base'

# Inicializa o SQLAlchemy com o app
db.init_app(app)

@app.route("/usuarios",methods=["GET"])
def seleciona_todos_Usuarios():

    usuarios_objeto = Usuarios.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objeto]

    if not usuarios_objeto:

        return handle_response(404, "usuarios", {},"Nenhum usuário encontrado")
    
    return handle_response(200, "usuarios", usuarios_json)

@app.route("/usuario/<id>",methods=["GET"])
def seleciona_usuario(id):

    usuario_objeto = Usuarios.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    if not usuario_objeto:

        return handle_response(404, "usuario", {},"Usuário não encontrado")
    
    return handle_response(200, "usuario", usuario_json)

@app.route("/criar.usuario",methods=["POST"])
def criar_usuario():

    body = request.get_json()

    try:
        usuario = Usuarios(nome=body["nome"],email=body["email"])
        db.session.add(usuario)
        db.session.commit()

        return handle_response(201, "usuario", usuario.to_json(),"Usuário criado com sucesso")
    
    except Exception as e:

        return handle_response(400, "usuario", {},f"Erro ao tentar criar usuario: {str(e)}")
    
@app.route("/atualizar.usuario/<id>",methods=["PUT"])
def atualizar_usuario(id):

    try:

        usuario_objeto = Usuarios.query.filter_by(id=id).first()

        if not usuario_objeto:

            return handle_response(404, "usuario", {},"Usuário não encontrado")
        
        body = request.get_json()

        # Lista de campos esperados para atualização
        campos_para_atualizar = ['nome', 'email']

        # Itera sobre os campos e atualiza apenas os presentes no body
        for campo in campos_para_atualizar:

            if campo in body:

                setattr(usuario_objeto, campo, body[campo])  # Atualiza dinamicamente o atributo

        db.session.commit()

        return handle_response(200, "usuario", usuario_objeto.to_json(),"Usuário atualizado com sucesso")
    
    except Exception as e:

        return handle_response(500, "usuario", {},f"Erro ao tentar atualizar usuário: {str(e)}")

@app.route("/deletar.usuario/<id>",methods=["DELETE"])
def deletar_usuario(id):
     
     try:
         
        usuario_objeto = Usuarios.query.filter_by(id=id).first()

        if not usuario_objeto:

            return handle_response(404, "usuario", {},"Usuário não encontrado")
        
        db.session.delete(usuario_objeto)
        db.session.commit()

        return handle_response(200, "usuario", usuario_objeto.to_json(),"Usuário deletado com sucesso")

     except Exception as e:
         
        return handle_response(400, "usuario", {},f"Erro ao tentar deletar usuário: {str(e)}")

app.run()


