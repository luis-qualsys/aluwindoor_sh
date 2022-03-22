from pprint import pprint
from urllib import response
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests as rq
import json

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
CORS(app)

@app.route('/api/v1')
def api_version():
    data = {
        'Version': 1.0,
        'Info': 'API de facturacion conecta con odoo'
    }
    response = jsonify(data)
    response.headers.set('Content-Type', 'application/json')
    # response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Credentials', 'true')
    return response, 200

@app.route('/web/session/authenticate', methods=['POST'])
def authenticate():
    try:
        if request.method == 'POST':
            payload = request.get_json()
            # pprint(dir(data))
            pprint(payload)
            url = "http://www.qualsys.com.mx:8099/web/session/authenticate"
            headers = {
                'Content-Type': 'application/json'
            }
            # headers = request.headers
            # print(headers)
            resp = rq.request("POST", url, headers=headers, data=json.dumps(payload))
            print(resp)
            print(resp.text)
            if resp.status_code == 200:
            # pprint(resp.cookies.get_dict())
                cookies = resp.cookies.get_dict()
                respon = resp.json()
                respon['session_id'] = cookies['session_id']
                response = jsonify(respuesta=respon)
                response.headers.set('Content-Type', 'application/json')
                # response.headers.set('Access-Control-Allow-Origin', '*')
                response.set_cookie('session_id', cookies['session_id'])
                return response, 200
            else:
                response = jsonify(error='No se obtuvo respuesta')
                return response, int(resp.status_code)
    except:
        return jsonify(respuesta={'error': 'Petición no aceptada verificar POST'}), 500

@app.route('/api/validate_sale', methods=['POST'])
def validate_sale():
    try:
        if request.method == 'POST':
            payload = request.get_json()
            # pprint(dir(data))
            pprint(payload)
            url = "http://www.qualsys.com.mx:8099/api/validate_sale"
            # headers = {
            #     'Content-Type': 'application/json',
            #     'X-Openerp': headers['X-Openerp']
            # }
            headers = request.headers
            print(payload)
            print(headers)
            cookies = {'username': 'admin', 'password': 'admin', 'session_id': headers['X-Openerp']}
            print(cookies)
            resp = rq.request("POST", url, headers=headers, data=json.dumps(payload), cookies=cookies)
            print(resp)
            print(resp.json())
            if resp.status_code == 200:
            # pprint(resp.cookies.get_dict())
                cookies = resp.cookies.get_dict()
                respon = resp.json()
                # respon['session_id'] = cookies['session_id']
                response = jsonify(respuesta=respon)
                response.headers.set('Content-Type', 'application/json')
                # response.headers.set('Access-Control-Allow-Origin', '*')
                # response.set_cookie('session_id', cookies['session_id'])
                return response, 200
            else:
                response = jsonify(error='No se obtuvo respuesta')
                return response, int(resp.status_code)
    except:
        return jsonify(respuesta={'error': 'Petición no aceptada verificar POST'}), 500


@app.route('/api/get_invoice', methods=['POST'])
def get_invoice():
    try:
        if request.method == 'POST':
            payload = request.get_json()
            # pprint(dir(data))
            print(request.get_json())
            # pprint(payload)
            url = "http://www.qualsys.com.mx:8099/api/get_invoice"
            # headers = {
            #     'Content-Type': 'application/json',
            #     'X-Openerp': headers['X-Openerp']
            # }
            headers = request.headers
            cookies = {'username': 'admin', 'password': 'admin', 'session_id': headers['X-Openerp']}
            print(headers)
            print(cookies)
            resp = rq.request("POST", url, headers=headers, data=json.dumps(payload), cookies=cookies)
            print(resp)
            print(resp.text)
            if resp.status_code == 200:
            # pprint(resp.cookies.get_dict())
                cookies = resp.cookies.get_dict()
                respon = resp.json()
                # respon['session_id'] = cookies['session_id']
                response = jsonify(respuesta=respon)
                response.headers.set('Content-Type', 'application/json')
                # response.headers.set('Access-Control-Allow-Origin', '*')
                # response.set_cookie('session_id', cookies['session_id'])
                return response, 200
            else:
                response = jsonify(error='No se obtuvo respuesta')
                return response, int(resp.status_code)
    except:
        return jsonify(respuesta={'error': 'Petición no aceptada verificar POST'}), 500


if __name__ == '__main__':
    app.run(debug=True)