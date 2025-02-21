from flask import Flask, render_template, jsonify
from datetime import datetime

from custom import Volume, Api, Analytics



# APP LOGIC


app = Flask(__name__)


def run_app():

    # Run the app on port 8000

    app.run(host='0.0.0.0', port=8000)


def up_to_date(stats):

    # Checks if the collected stats are up to date (from the same day as today's date)

    if not stats:
        return False

    stats_date = datetime.strptime(stats['header']['date'], '%d-%m-%y')
    today = datetime.today()

    same_day = (
        stats_date.year == today.year and
        stats_date.month == today.month and
        stats_date.day == today.day
        )
    
    return same_day




# VIEWS ROUTES
    

@app.route('/')
def index_main():
    return render_template('stats.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')




# API ROUTES


@app.route('/get_player_data/', methods=['GET'])
def get_player_data():

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