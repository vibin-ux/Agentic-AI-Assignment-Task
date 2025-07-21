from langchain.tools import tool
from fetch_recap import fetch_last_20_gsw_night_games, get_gsw_team_id
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import json

def save_recap_to_cache(recap_url, recap_text, filename="recap_cache.json"):
    cache = load_recap_from_cache(filename) or {}
    cache[recap_url] = recap_text
    with open(filename, "w") as f:
        json.dump(cache, f)

def load_recap_from_cache(filename="recap_cache.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None

@tool
def get_night_games_info(input: str) -> str:
    """
    Returns the last 20 Golden State Warriors night games with opponent, date, and recap URL.
    """
    games = fetch_last_20_gsw_night_games()
    if not games:
        return "No night games found."
    
    lines = []
    for g in games:
        line = f"{g['date']} ➜ {g['opponent']} ➜ Recap: {g['recap_url']}"
        lines.append(line)
    return "\n".join(lines)

@tool
def fetch_game_recap(recap_url: str) -> str:
    """
    Uses Selenium to fetch full NBA recap text from a JavaScript-rendered NBA.com article.
    Input: recap_url (str) — The NBA.com recap link
    Output: Full recap text (up to 3000 characters)
    """
    cached_recaps = load_recap_from_cache()
    if cached_recaps and recap_url in cached_recaps:
        return cached_recaps[recap_url]

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(recap_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article p"))
        )

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = "\n".join(p.text.strip() for p in paragraphs if len(p.text.strip()) > 40)

        driver.quit()
        save_recap_to_cache(recap_url, content)
        return content[:3000] if content else "No usable recap content found."
    except Exception as e:
        return f"Error using selenium: {str(e)}"
    
from nba_api.stats.endpoints import boxscoreadvancedv2
from fetch_recap import get_gsw_team_id

def get_fast_break_stats(game_id: str) -> str:
    """
    Fetches fast-break points for a given game ID.
    Input: game_id (str) — NBA game ID
    Output: Fast-break points for GSW and opponent
    """
    try:
        boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id).get_data_frames()[0]
        gsw_stats = boxscore[boxscore['TEAM_ID'] == get_gsw_team_id()].iloc[0]
        opp_stats = boxscore[boxscore['TEAM_ID'] != get_gsw_team_id()].iloc[0]
        return (f"GSW Fast-Break Points: {int(gsw_stats['PTS_FB'])}, "
        f"Opponent Fast-Break Points: {int(opp_stats['PTS_FB'])}")
    except Exception as e:
        return f"Error fetching fast-break stats: {str(e)}"
