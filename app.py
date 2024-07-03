from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suprimir avisos de solicitações sobre verificações de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'yrpreyapi'

# Conexão com o banco de dados
db = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)

@app.route('/01', methods=['POST'])
def search_user():
    # Recebe os dados JSON da requisição
    request_data = request.get_json()

    if 'name' in request_data and 'id' in request_data:
        name = request_data['name']
        id = request_data['id']

        # Executa a consulta SQL para encontrar o usuário pelo nome
        cursor = db.cursor()
        cursor.execute("SELECT * FROM team WHERE nome LIKE %s", ('%' + name + '%',))
        rows = cursor.fetchall()

        if rows:
            response = {
                'status': 'success',
                'users': []
            }

            for row in rows:
                owner = "no"
                xpl = "yes"

                if str(id) == str(row["user_id"]):
                    owner = "yes"
                    xpl = "no"

                user_data = {
                    'name': row["nome"],
                    'owner': owner,
                    'type': xpl,
                    'message': 'User found: ' + str(id)
                }

                response['users'].append(user_data)
        else:
            response = {
                'status': 'error',
                'message': 'No users found with name: ' + name
            }
    else:
        response = {
            'status': 'error',
            'message': 'Name or id not provided in request'
        }

    # Retorna a resposta como JSON
    return jsonify(response)

@app.route('/02', methods=['POST'])
def login():
    # Configura o cabeçalho de resposta como JSON
    response_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Access-Control-Allow-Credentials': 'true'
    }

    # Obtém os dados JSON da requisição POST
    data = request.json

    # Verifica se os campos necessários estão presentes nos dados recebidos
    if 'username' in data and 'password' in data and 'token' in data:
        username = data['username']
        password = data['password']
        token = data['token']

        # Consulta no banco de dados para verificar se o usuário existe
        try:
            with db.cursor() as cursor:
                sql = "SELECT * FROM `user` WHERE (username=%s AND password=%s) OR token=%s"
                cursor.execute(sql, (username, password, token))
                row = cursor.fetchone()

                if not row:
                    response = {
                        'status': 'error',
                        'msg': 'Name not found'
                    }
                else:
                    response = {
                        'status': 200,
                        'username': row['username'],
                        'token': row['token'],
                        'role': row['role'],
                        'msg': 'Register found'
                    }
        except Exception as e:
            response = {
                'status': 'error',
                'message': f'Database error: {str(e)}'
            }
    else:
        response = {
            'status': 'error',
            'message': 'Name, password, or token not provided'
        }

    return jsonify(response), 200, response_headers    

@app.route('/03', methods=['POST'])
def verify_user():
    # Configura os cabeçalhos de resposta
    response_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Access-Control-Allow-Credentials': 'true'
    }

    # Obtém os dados JSON da requisição POST
    data = request.json

    # Verifica se os campos necessários estão presentes nos dados recebidos
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']

        try:
            with db.cursor() as cursor:
                # Verifica se o usuário existe no banco de dados
                sql = "SELECT * FROM `user` WHERE username=%s AND password=%s"
                cursor.execute(sql, (username, password))
                row = cursor.fetchone()

                if not row:
                    # Se o usuário não for encontrado, seleciona um usuário aleatório
                    query = """
                        SELECT * FROM `user`
                        WHERE id >= (SELECT FLOOR(MAX(id) * RAND()) FROM `user`)
                        ORDER BY id LIMIT 1
                    """
                    cursor.execute(query)
                    random_row = cursor.fetchone()

                    response = {
                        'status': 'error',
                        'token': random_row['token'],
                        'msg': 'Name not found'
                    }
                else:
                    response = {
                        'status': 200,
                        'username': row['username'],
                        'token': row['token'],
                        'role': row['role'],
                        'msg': 'Register found'
                    }

        except Exception as e:
            response = {
                'status': 'error',
                'message': f'Database error: {str(e)}'
            }
    else:
        response = {
            'status': 'error',
            'message': 'Name not provided'
        }

    return jsonify(response), 200, response_headers

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'yrpreyapi',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/04', methods=['GET'])
def get_images():
    # Cabeçalhos CORS
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    img = int(request.args.get('img', 1))

    images = []

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        for _ in range(img + 1):
            query = "SELECT url FROM images"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                images.append(result['url'])
            else:
                images.append("http://localhost/img/logo.webp")

        cursor.close()
        connection.close()
    except Exception as e:
        return jsonify({'error': f'Erro de conexão: {str(e)}'}), 500, response_headers

    return jsonify(images), 200, response_headers 
    

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'yrpreyapi',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/05', methods=['POST'])
def check_user():
    # Cabeçalhos CORS
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Credentials": "true"
    }

    # Verificar e obter dados JSON da solicitação
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Invalid JSON: {str(e)}'}), 400, response_headers

    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400, response_headers

    if 'token' in data and 'role' in data:
        token = data['token']
        role = data['role']

        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            query = "SELECT * FROM user WHERE token LIKE %s OR role = %s"
            cursor.execute(query, ('%' + token + '%', role))
            row = cursor.fetchone()
            exist = cursor.rowcount

            if exist > 0:
                response_data = {
                    'status': 'success',
                    'name': row["username"],
                    'owner': row["role"],
                    'token': row["token"],
                    'message': 'User found: ' + token
                }
            else:
                response_data = {
                    'status': 'error',
                    'message': 'User not found'
                }

            cursor.close()
            connection.close()
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': f'Error: {str(e)}'
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Token or role not provided'
        }

    response = jsonify(response_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    response.headers.add("Access-Control-Allow-Credentials", "true")

    return response, 200, response_headers



@app.route('/06', methods=['POST'])
def validate():
    # Configura o cabeçalho de resposta como JSON e permite CORS
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Credentials": "true"
    }

    data = request.get_json()

    if 'validate' in data:
        url = data['validate']

        if url == "localhost":
            return jsonify("200 OK"), 200, response_headers
        else:
            try:
                response = requests.get(url)
                result = response.text
                headers = response.headers

                return jsonify(result=result, headers=dict(headers)), 200, response_headers
            except requests.exceptions.RequestException as e:
                return jsonify(error=str(e)), 500, response_headers
    else:
        return jsonify(error="No validate key provided in the request"), 400, response_headers

@app.route('/v2/08', methods=['POST'])

def search_user_v2():

    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Credentials": "true"
    }
        
    # Recebe os dados JSON da requisição
    data = request.get_json()

    if 'name' in data:
        name = data['name']

        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # Consulta SQL para buscar usuários com nome semelhante
            query = "SELECT * FROM user WHERE username LIKE %s"
            cursor.execute(query, ('%' + name + '%',))

            # Busca todos os resultados
            results = cursor.fetchall()

            if results:
                response = results
            else:
                response = {'status': 'error', 'message': 'Name not found'}

            cursor.close()
            connection.close()

        except Exception as e:
            response = {'status': 'error', 'message': f'Error: {str(e)}'}

    else:
        response = {'status': 'error', 'message': 'Name not provided'}

    # Retorna a resposta como JSON
    return jsonify(response)

@app.route('/v1/08', methods=['POST'])

def search_user_v5():

    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Credentials": "true"
    }
        
    # Recebe os dados JSON da requisição
    data = request.get_json()

    if 'name' in data:
        name = data['name']

        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # Consulta SQL para buscar usuários com nome semelhante
            query = "SELECT * FROM user"
            cursor.execute(query)

            # Busca todos os resultados
            results = cursor.fetchall()

            if results:
                response = results
            else:
                response = {'status': 'error', 'message': 'Name not found'}

            cursor.close()
            connection.close()

        except Exception as e:
            response = {'status': 'error', 'message': f'Error: {str(e)}'}

    else:
        response = {'status': 'error', 'message': 'Name not provided'}

    # Retorna a resposta como JSON
    return jsonify(response)

@app.route('/07', methods=['POST'])
def handle_request():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(dict(headers))

if __name__ == '__main__':
    app.run(port=5000)
