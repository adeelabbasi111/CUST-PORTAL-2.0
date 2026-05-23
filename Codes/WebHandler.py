from flask import Flask
from utils.web_routes import register_routes

class WebHandler:
    def __init__(self, data_folder="StudentData", driver=None):
        self.app = Flask(__name__)
        self.DATA_FOLDER = data_folder
        self.driver = driver
        self._setup_routes()

    def _setup_routes(self):
        register_routes(self.app, self.driver)

    def run(self, debug=False, host='127.0.0.1', port=5000):
        self.app.run(debug=debug, use_reloader=False, host=host, port=port)