import json
from flask import Response

def handle_response(status, nome_do_conteudo, conteudo, mensagem=False):
    
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")
