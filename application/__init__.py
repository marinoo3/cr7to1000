from flask import Flask  
import os

from .custom import Api, Analytics
from .models import Database




def create_app():

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    with app.app_context():
        app.secret_key = os.environ.get('CR7TO1000_SECRET_KEY')
        app.api = Api()
        app.analytics = Analytics()
        app.database = Database()


    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .endpoints import endpoints as endpoints_blueprint
    app.register_blueprint(endpoints_blueprint, url_prefix='/api')


    return app