from operations.connector_database import db

class Usuarios(db.Model):

    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

    