from flask import Flask, render_template, send_from_directory, jsonify

from custom import Database, Api, Analytics
from custom.utils import up_to_date

import os



# APP LOGIC


app = Flask(__name__)
app.secret_key = "0923876591023"


def run_app():

    # Run the app on port 8000
    app.run(host='0.0.0.0', port=8000)




# VIEWS ROUTES
    

@app.route('/')
def index_main() -> str:
    return render_template('stats.html')

@app.route('/privacy-policy')
def privacy_policy() -> str:
    return render_template('privacy-policy.html')

@app.route('/robots.txt')
def robots() -> str:
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap() -> str:
    return send_from_directory(app.static_folder, 'sitemap.xml')




# API ROUTES


@app.route('/get_player_data/', methods=['GET'])
def get_player_data() -> Flask.response_class:

    # collect stats from saved volume
    stats = DATABASE.get_dashboard_stats()

    # if stats not up to date then scrap, analyse and save stats to volume
    if not up_to_date(stats['last_update']):
        data = API.get_data()
        stats = ANALYTICS.format_stats(data)
        DATABASE.save_dashboard_stats(stats)

    return jsonify(stats)




# INIT

DATABASE = Database()
API = Api()
ANALYTICS = Analytics()

if __name__ == '__main__':
    run_app()
