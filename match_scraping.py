import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/sport/football/scores-fixtures"
HEADERS = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0" }
DEFAULT_TEAMS_DIR = "files/default_teams.txt"

def load_default_teams ():
    f = open(DEFAULT_TEAMS_DIR, 'r')
    teams = f.readlines()
    return [t.strip() for t in teams]

# TODO
"""
def load_css_url ():
    pass
"""

all_teams = load_default_teams()

def get_response_and_soup ():
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_matches_by_team (followed_teams):
    soup = get_response_and_soup ()
    competition_blocks = soup.find_all(class_="qa-match-block")
    relevant_matches = []
        
    for comp_block in competition_blocks:
        match_blocks = comp_block.find_all(class_="gs-o-list-ui__item gs-u-pb-")
        competition = comp_block.find(class_="gel-minion sp-c-match-list-heading").get_text()

        for mb in match_blocks:
            teams = mb.find_all(class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
            teams = [t.get_text() for t in teams]
            
            match_is_relevant = False
            for s in followed_teams:
                if s == teams[0] or s == teams[1]:
                    match_is_relevant = True
                    break
                
            if match_is_relevant:
                match_string = create_match_string(mb, competition, teams)
                relevant_matches.append(match_string)
                    
    return relevant_matches

def create_match_string (match_block, competition, teams):

    match_time = match_block.find(class_="sp-c-fixture__number sp-c-fixture__number--time")
    
    if match_time == None:
        elapsed_game_time = match_block.find(class_="sp-c-fixture__status gel-brevier sp-c-fixture__status--live-sport")

        if elapsed_game_time is not None:
            match_string = "{} vs {}, have been playing for {}".format(teams[0], teams[1], elapsed_game_time.get_text())
        else:
            match_string = "{} vs {}, have already played".format(teams[0], teams[1])
    else:
        match_string = "{} vs {}, at {}".format(teams[0], teams[1], match_time.get_text())

    return match_string, competition
