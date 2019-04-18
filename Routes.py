from Utilities.Database import reg_cache, scheduler, Client
from flask import Blueprint, request, jsonify, abort
from Utilities.Scheduler import DoesNotExist
import time


@mod.route('/register')
def register():

    client = Client()
    reg_cache[client.client_id] = client

    return jsonify({
        "client_id": client.peer.id_hex,
        "private_id": client.peer.key_hex,
        "timestamp": time()
    })

@mod.route('/verify')
def verify():

    body = request.json
    if 'client_id' not in body or 'private_id' not in body:
        return abort(400)

    client_id = body['client_id']
    private_id = body['private_id']

    client = scheduler.get(client_id)
    if not client:
        return abort(404)

    if client.peer.key_hex != private_key:
        return abort(401)

    result = scheduler.verify(client_id)
    if not result:
        return abort(400, 'not a valid request')

    return jsonify({
        "client_id": client.peer.id_hex,
        "verified": True,
        "timestamp": time()
    })

@mod.route('/logout')
def logout():
    pass

@mod.route('/peer/<client_id>/udp/status')
def get_client_status(client_id):
    pass

@mod.route('/peer/<client_id>/udp/address')
@mod.route('/peer/<client_id>/udp')
def get_client_udp_address(client_id):
    pass
