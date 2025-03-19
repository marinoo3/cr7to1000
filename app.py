from flask import Flask, render_template, send_from_directory, jsonify

from custom import Volume, Api, Analytics
from custom.utils import up_to_date



# APP LOGIC


app = Flask(__name__)


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
def robots_txt() -> str:
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap() -> str:
    return send_from_directory(app.static_folder, 'sitemap.xml')




# API ROUTES


@app.route('/get_player_data/', methods=['GET'])
def get_player_data() -> Flask.response_class:

    # collect stats from saved volume
    stats = VOLUME.get_stats()

    # if stats not up to date then scrap, analyse and save stats to volume
    if not up_to_date(stats):
        data = API.get_data()
        stats = ANALYTICS.format_stats(data)
        VOLUME.save_stats(stats)

    return jsonify(stats)




# INIT

VOLUME = Volume()
API = Api()
ANALYTICS = Analytics()

if __name__ == '__main__':
    run_app()