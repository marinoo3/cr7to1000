from flask import Blueprint, jsonify, request, current_app
from .utils import up_to_date




endpoints = Blueprint('api', __name__)




@endpoints.route('/get_dashboard_data/', methods=['GET'])
def get_dashboard_data():

    last_update = current_app.database.get_last_update(stats='all_stats')

    if not up_to_date(last_update):
        data = current_app.api.get_data()
        stats_data = current_app.analytics.format_stats(data)
        current_app.database.save_stats(stats_data)

    stats = current_app.database.get_dashboard_stats()

    return jsonify(stats)


@endpoints.route('/get_goals_data/', methods=['GET'])
def get_goals_data():

    offset = request.args.get('offset', default=0, type=int)

    last_update = current_app.database.get_last_update(stats='all_stats')

    if not up_to_date(last_update):
        data = current_app.api.get_data()
        stats_data = current_app.analytics.format_stats(data)
        current_app.database.save_stats(stats_data)

    stats = current_app.database.get_goals_stats(offset=offset)

    return jsonify(stats)