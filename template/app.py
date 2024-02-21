from flask import Flask, render_template
import pandas as pd
from test import get_standings_table, get_team_urls, get_team_matches, get_team_shooting_stats

app = Flask(__name__)

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
standings_table = get_standings_table(standings_url)
team_urls = get_team_urls(standings_table)

@app.route('/')
def index():
    return render_template('index.html', team_urls=team_urls)

@app.route('/team/<int:team_index>')
def team_details(team_index):
    if 0 <= team_index < len(team_urls):
        team_matches = get_team_matches(team_urls[team_index])
        shooting_stats = get_team_shooting_stats(team_urls[team_index])
        return render_template('team_details.html', team_matches=team_matches, shooting_stats=shooting_stats)
    else:
        return "Invalid team index."

if __name__ == '__main__':
    app.run(debug=True)
