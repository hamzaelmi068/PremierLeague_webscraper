import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_standings_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    standings_table = soup.select_one('table.stats_table')
    return standings_table

def get_team_urls(standings_table):
    links = standings_table.select('a[href^="/squads/"]')
    team_urls = [f"https://fbref.com{l['href']}" for l in links]
    return team_urls

def get_team_matches(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = pd.read_html(response.text, match="Scores & Fixtures")[0]
    return matches

def get_team_shooting_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [l['href'] for l in soup.find_all('a', href=lambda x: x and 'all_comps/shooting/' in x)]
    shooting_stats_url = f"https://fbref.com{links[0]}"
    shooting_stats = pd.read_html(requests.get(shooting_stats_url).text, match="Shooting")[0]
    return shooting_stats

def main():
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    
    # Get standings table
    standings_table = get_standings_table(standings_url)

    # Get team URLs
    team_urls = get_team_urls(standings_table)

    if not team_urls:
        print("No team URLs found.")
        return

    # Get matches for the first team
    team_matches = get_team_matches(team_urls[0])
    print("Matches for the first team:")
    print(team_matches)

    # Get shooting stats for the first team
    shooting_stats = get_team_shooting_stats(team_urls[0])
    print("\nShooting stats for the first team:")
    print(shooting_stats.head())

if __name__ == "__main__":
    main()
