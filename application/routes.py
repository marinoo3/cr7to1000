from flask import Blueprint, render_template, send_from_directory



main = Blueprint('main', __name__)



@main.route('/')
@main.route('/dashboard')
def index_dashboard():
    return render_template('dashboard.html')

@main.route('/goals')
def index_goals():
    return render_template('goals.html')

@main.route('/videos')
def index_videos():
    return render_template('videos.html')

@main.route('/bio')
def index_bio():
    return render_template('biographie.html')

@main.route('/privacy-policy')
def index_privacy_policy():
    return render_template('privacy-policy.html')

@main.route('/robots.txt')
def index_robots():
    return send_from_directory('static', 'robots.txt')

@main.route('/sitemap.xml')
def index_sitemap():
    return send_from_directory('static', 'sitemap.xml')