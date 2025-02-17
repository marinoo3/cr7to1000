from flask import Flask, render_template, jsonify

from custom import flashscore



# APP LOGIC


app = Flask(__name__)

def run_app():
    app.run(host='0.0.0.0', port=8000)





# VIEWS ROUTES
    

@app.route('/')
def index_main():
    return render_template('stats.html')




# API ROUTES


@app.route('/get_player_data/', methods=['GET'])
def get_player_data():
    stats = API.get_player_stat(name='ronaldo-cristiano', id='WGOY4FSt')
    return jsonify({'stats': stats})


# INIT

API = flashscore.FlashScore()
run_app()