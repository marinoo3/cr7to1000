from flask import Flask, render_template, send_from_directory, jsonify
import locale

from custom import Database, Api, Analytics
from custom.utils import up_to_date

import os



# APP LOGIC


app = Flask(__name__)
app.secret_key = os.environ.get('CR7TO1000_SECRET_KEY')
locale.setlocale(locale.LC_TIME, 'fr_FR')


def run_app():

    # Run the app on port 8000
    app.run(host='0.0.0.0', port=8000)




# VIEWS ROUTES
    

@app.route('/')
def index_main() -> str:
    return render_template('dashboard.html')

@app.route('/dashboard')
def index_dashboard() -> str:
    return render_template('dashboard.html')

@app.route('/goals')
def index_goals() -> str:
    return render_template('goals.html')

@app.route('/videos')
def index_videos() -> str:
    return render_template('videos.html')

@app.route('/privacy-policy')
def index_privacy_policy() -> str:
    return render_template('privacy-policy.html')

@app.route('/robots.txt')
def index_robots() -> str:
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def index_sitemap() -> str:
    return send_from_directory(app.static_folder, 'sitemap.xml')




# API ROUTES


@app.route('/get_dashboard_data/', methods=['GET'])
def get_dashboard_data() -> Flask.response_class:

    # check last update date
    last_update = DATABASE.get_last_update(stats='all_stats')
    # if stats not up to date then scrap, analyse and save stats to volume
    if not up_to_date(last_update):
        data = API.get_data()
        stats_data = ANALYTICS.format_stats(data)
        DATABASE.save_stats(stats_data)
    
    # collect stats from saved volume
    stats = DATABASE.get_dashboard_stats()

    return jsonify(stats)

@app.route('/get_goals_data/', defaults={'offset': 0}, methods=['GET']) #optional offset parameter, default is 0
@app.route('/get_goals_data/<offset>', methods=['GET'])
def get_goals_data(offset) -> Flask.response_class:

    # check last update date
    last_update = DATABASE.get_last_update(stats='all_stats')
    # if stats not up to date then scrap, analyse and save stats to volume
    if not up_to_date(last_update):
        data = API.get_data()
        stats_data = ANALYTICS.format_stats(data)
        DATABASE.save_stats(stats_data)

    # collect stats from saved volume
    stats = DATABASE.get_goals_stats(offset=offset)

    return jsonify(stats)




# INIT

DATABASE = Database()
API = Api()
ANALYTICS = Analytics()

if __name__ == '__main__':
    run_app()