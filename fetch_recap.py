import requests
from datetime import datetime
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
import pytz

def get_gsw_team_id():
    gsw = [team for team in teams.get_teams() if team['full_name'] == 'Golden State Warriors']
    return gsw[0]['id'] if gsw else None

def is_night_game(start_time_utc_str, timezone='America/Los_Angeles'):
    try:
        local_time = datetime.strptime(start_time_utc_str, "%Y-%m-%dT%H:%M:%SZ")
        local_tz = pytz.timezone(timezone)
        local_time = local_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_time.hour >= 18  # Night game if 6PM or later
    except Exception as e:
        print(f"[ERROR] Failed to parse time: {e}")
        return False

def fetch_last_20_gsw_night_games():
    gsw_team_id = get_gsw_team_id()
    if not gsw_team_id:
        print("[ERROR] Could not find GSW team ID.")
        return []

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=gsw_team_id)
    games = gamefinder.get_data_frames()[0]

    night_games = []
    for _, game in games.iterrows():
        game_date = game['GAME_DATE']
        matchup = game['MATCHUP']
        game_id = game['GAME_ID']

        # Fetch start time via NBA.com JSON endpoint
        url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                start_time_utc = data.get('game', {}).get('gameTimeUTC')
                if start_time_utc and is_night_game(start_time_utc):
                    night_games.append({
                        'game_id': game_id,
                        'date': game_date,
                        'opponent': matchup,
                        'start_time_utc': start_time_utc,
                        'recap_url': f"https://www.nba.com/game/{game_id}/recap"
                    })
        except Exception as e:
            print(f"[ERROR] Checking game {game_id}: {e}")

        if len(night_games) == 20:
            break

    return night_games

if __name__ == "__main__":
    games = fetch_last_20_gsw_night_games()
    print("=== GSW Night Games ===")
    for g in games:
        print(f"{g['date']} ➜ {g['opponent']} ➜ {g['recap_url']}")
