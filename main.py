from flask import Flask
from Controllers.Controller import Controller
from Controller.UDPHeartbeat import UDPHeartbeat
import Routes


app = Flask(__name__)
app.register_blueprint(Routes.mod)


if __name__ == '__main__':

    Controller.start_scheduler()
    UDPHeartbeat.start_running(port=5024)
    app.run(host="0.0.0.0", port=5025)
