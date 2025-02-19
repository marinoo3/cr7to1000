from flask import Flask, render_template, jsonify
from datetime import datetime

from custom import Volume, TransferMarkt, Analytics



# APP LOGIC


app = Flask(__name__)

def run_app():
    app.run(host='0.0.0.0', port=8000)


def up_to_date(stats):

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




# API ROUTES


@app.route('/get_player_data/', methods=['GET'])
def get_player_data():

    stats = VOLUME.get_stats()

    if not up_to_date(stats):
        data = API.get_player_stat()
        stats = ANALYTICS.format_stats(data)
        VOLUME.save_stats(stats)

    return jsonify(stats)




# INIT

VOLUME = Volume()
API = TransferMarkt()
ANALYTICS = Analytics()
