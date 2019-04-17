# Socket Rendezvous Server
A general purpose socket Rendezvous server for managing and implementing peer to peer connections.


## UDP Heartbeating
- Port: 5024
- Heartbeat Interval: 30 seconds
- Error Time: 3 minutes
##### Payload Design
```
# Length must be in Big Endian format
| 1 byte length of address | address | 
```

##### Response
```
Response code is in Big Endian format
| 1 byte response code |
```
#### Response Codes
**1020**: Pulse was successful and on time\
**1050**: Must re-verify you're address\
**1060**: Client address was not found\

# Routes
### Register a new Client
Register a new client on the server\
**Route**: `/register`\
**Method** : `POST`\
**Port** : `5025`

**Response**:
```json
{
    "client_id": "hex string",
    "private_id": "hex string",
    "timestamp": "unix timestamp"
}
```

### Re-Verify a Client
Re-Verify the client address after not being responsive for less than\
(Error Time) + (1 x Pulse Interval)\
**Route**: `/verify`\
**Method** : `POST`\
**Port** : `5025`

**Request Body**:
```json
{
    "client_id": "hex string",
    "private_id": "hex string"
}
```

**Response**:
```json
{
    "client_id": "hex string",
    "verified": true,
    "timestamp": "unix timestamp"
}
```

### Logout the Client
Logout the client from the Server\
**Route**: `/logout`\
**Method** : `POST`\
**Port** : `5025`

**Request Body**:
```json
{
    "private_id": "hex string"
}
```

**Response**:
```json
{
    "client_id": "hex string",
    "ok": true
}
```

### Get another Client's UDP Address
Get another client's UDP address to perform peer to peer connection\
**Route**: `/peer/<client_id>/udp`\
**Method** : `GET`\
**Port** : `5025`

**Query Parameters**
- client_id: Target's client id
- private_key: Requester's private key for authentication

**Response**:
```json
{
    "client_id": "hex string",
    "host": "ipv4 host address",
    "port": "int",
    "timestamp": "unix timestamp"
}
```
### Get another Client's status
Get the time interval since the last pulse from the target\
**Route**: `/peer/<client_id>/udp/status`\
**Method** : `GET`\
**Port** : `5025`

**Query Parameters**
- client_id: Target's client id
- private_key: Requester's private key for authentication

**Response**:
```json
{
    "client_id": "hex string",
    "status": "ONLINE, PENDING",
    "last_online": "seconds since last pulse",
    "timestamp": "unix timestamp"
}
```
**Status Values**
- ONLINE: the client has been pulsing the server on the correct intervals\
- PENDING: the client has not sent a pulse to the server for over the default Pulse Interval and the server is waiting for the fixed Error time before loging out the client from the server.

