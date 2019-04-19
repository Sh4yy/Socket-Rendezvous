from flask import Blueprint, jsonify, abort, g
from Utilities.Decorators import authorized
from Controllers.Controller import Controller
from time import time


mod = Blueprint('routes', __name__)


@mod.route('/register')
def register():

    client = Controller.register()

    return jsonify({
        "client_id": client.peer.id_hex,
        "private_id": client.peer.key_hex,
        "timestamp": time(),
        "ok": True
    })


@mod.route('/verify')
@authorized
def verify():

    client_id, private_id = g.client_id, g.private_id
    result = Controller.verify(client_id, private_id)

    return jsonify({
        "client_id": client_id,
        "timestamp": time(),
        "ok": result
    })


@mod.route('/logout')
@authorized
def logout():
    
    client_id, private_id = g.client_id, g.private_id
    result = Controller.logout(client_id, private_id)

    return jsonify({
            "client_id": client_id,
            "ok": result
        })


@mod.route('/peer/<client_id>/udp/status')
@authorized
def get_client_status(client_id):

    client = Controller.get_client(client_id)
    if not client:
        return abort(404)

    return jsonify({
        "client_id": client_id,
        "status": client.status.value,
        "last_online": client.last_pulse,
        "timestamp": time(),
        "ok": True
    })


@mod.route('/peer/<client_id>/udp/address')
@mod.route('/peer/<client_id>/udp')
@authorized
def get_client_udp_address(client_id):

    client = Controller.get_client(client_id)
    if not client:
        return abort(404)

    host, port = client.get_address()
    if not host or not port:
        return abort(404)

    return jsonify({
        "client_id": client_id,
        "host": host,
        "port": port,
        "timestamp": time(),
        "ok": True
    })
