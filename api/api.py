from bson.objectid import ObjectId
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask.json import dumps
from flask_cors import CORS, cross_origin
from mongita import MongitaClientDisk
from unidecode import unidecode
import mongita
from bson.json_util import dumps, loads
from datetime import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

now = datetime.now()

client = MongitaClientDisk()

db = client.db_transferencia
coll_user = db.usuario
coll_tranferencia = db.transferencia

def nova_transferencia(dados):
    info = dados.decode('ascii')
    info = loads(info)
    
    id = list(coll_user.find({'nome': info['pagador_nome']}))
    
    info['usuario_id'] = id[0]['id']
    
    if info['pagador_banco'] == info['beneficiario_banco']:
        info['tipo'] = 'CC'
    elif int(info['valor']) < 5000:
        info['tipo'] = 'TED'
    else:
        info['tipo'] = 'DOC'
    
    if int(info['valor']) > 100000:
        info['status'] = 'ERRO'
    else:
        info['status'] = 'OK'
        
    info['mostrar'] = True
    
    print(info)
        
    coll_tranferencia.insert_one(info)
    
    return dumps('Tranferencia realizada')

def apagar_transferencia(id):
    info = id.decode('ascii')
    coll_tranferencia.update_one({'_id': ObjectId(info)}, {'$set': {'mostrar': False}})
    
def listar_transferencia():
    dados = list(coll_tranferencia.find({'mostrar': True}))
    
    return dumps(dados)

def novo_cliente(dados):
    info = dados.decode('ascii')
    info = loads(info)
    
    coll_user.insert_one(info)
    
    return dumps('Usuário cadastrado')

def listar_clientes():
    dados = list(coll_user.find({})) 
    
    return dumps(dados)
    
@app.route('/nova', methods=['POST'])
@cross_origin()
def run_nova_transferencia():
    try:
        return Response(status=200, response=nova_transferencia(request.data))
    except Exception as e:
        return Response(status=400)

@app.route('/delete', methods=['POST'])
@cross_origin()
def run_apagar_transferencia():
    try:
        return Response(status=200, response=apagar_transferencia(request.data))
    except Exception as e:
        return Response(status=400)
    
@app.route('/listar', methods=['GET'])
@cross_origin()
def run_listar_transferencia():
    try:
        return Response(status=200, response=listar_transferencia())
    except Exception as e:
        return Response(status=400)
    
@app.route('/novo_cliente', methods=['POST'])
@cross_origin()
def run_novo_cliente():
    try:
        return Response(status=200, response=novo_cliente(request.data))
    except Exception as e:
        return Response(status=400)

@app.route('/listar_clientes', methods=['GET'])
@cross_origin()
def run_listar_clientes():
    try:
        return Response(status=200, response=listar_clientes())
    except Exception as e:
        return Response(status=400)

if __name__ == '__main__':
    CORS(app)
    app.run(use_reloader=True)