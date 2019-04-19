from flask import Flask
from Controllers.Controller import Controller
from Controllers.UDPHeartbeat import UDPHeartbeat
import Routes


app = Flask(__name__)
app.register_blueprint(Routes.mod)


if __name__ == '__main__':

    Controller.start_scheduler()
    udp_heartbeat = UDPHeartbeat(host="0.0.0.0", port=5027)
    udp_heartbeat.start_running()
    app.run(host="0.0.0.0", port=5025, debug=True, use_reloader=False)
