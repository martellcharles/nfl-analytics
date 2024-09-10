"""
This module provides functions for scraping offensive player data to add to database.
"""
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import pickle
import io
import os

# this dict of player links will be used to pull the player data, the dateframe contains 
def pull_player_links() -> dict:
    """
        Grabs the player links for the current season with any recorded rushing, receiving, or passing stat.
        Saves new links to player_links pickle file, although not currently using file for anything.
        
        Args:
            Nothing

        Returns:
            current season player links for all players with recorded stats
    """
    year = os.environ.get("NFL_SEASON")
    links_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_links.pkl"
    curr_year_links = {}
    with open(links_path, 'rb') as dickle:
        links = pickle.load(dickle)
    for statistic in ['passing', 'rushing', 'receiving']:
        # scrapes table from site and waits to ensure we don't send too many requests to the site
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + statistic + ".htm"
        try:
            page = requests.get(url)
        except:
            print(url)
        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(3)
        rows = soup.find("table").find("tbody").find_all("tr")
        # this table contains the season totals for every player we gather, saving us some calculation later
        df = pd.read_html(io.StringIO(str(soup.find("table"))))[0]
        # assigns variables needed for loop to function
        if statistic == 'rushing':
            fix_double_level_columns(df)
        for idx, row in enumerate(rows):
            # grabs element of row that contains the player link
            # rushing, receiving, and passing pages are formatted differently
            if statistic == 'rushing':
                if df.loc[idx, ('Game Info', 'Player')] == 'Player':
                    continue
                link = row.find('td', {'data-stat':'player'})['data-append-csv']
                player = df.loc[idx, ('Game Info', 'Player')]
            elif statistic == 'receiving':
                if df.loc[idx, 'Player'] == 'Player':
                    continue
                link = row.find('td', {'data-stat':'player'})['data-append-csv']
                player = df.loc[idx, 'Player']
            else:
                link_father = row.find('td', {'data-stat':'name_display'})
                if link_father['csk'] == 'zzzzz':
                    continue
                link = link_father.find('a').get('href').split('/')[3].split('.')[0]
                player = df.loc[idx, 'Player']
            if player not in links:
                links[player] = link
            curr_year_links[player] = link
    with open(links_path, 'wb') as dickle:
        pickle.dump(links, dickle)
    return curr_year_links


def fix_double_level_columns(df: pd.DataFrame) -> None:
    """
        If table is scraped with multi column indices, this code cleans up the column names who were scraped weird.
        
        Args:
            individual player stats (pandas DataFrame): stats of every game player has played in current season

        Returns:
            Nothing, dataframe is edited in place
    """
    col1 = {}
    col2 = {}
    for i in df.columns:
        if "Unnamed:" in i[0]:
            col1[i[0]] = 'Game Info'
        if "Unnamed:" in i[1]:
            col2[i[1]] = 'H/A'
    df.rename(columns=col1, level=0, inplace=True)
    df.rename(columns=col2, level=1, inplace=True)

def clean_player_df(df: pd.DataFrame) -> None:
    """
        Cleans individual player dataframe to allow combining of all player dfs
        Breaks results col into 3; result, home_score, away_score as well as reformats home/away col
        
        Args:
            individual player stats (pandas DataFrame): stats of every game player has played in current season

        Returns:
            Nothing, dataframe is edited in place
    """
    if df.columns.nlevels == 2:
        fix_double_level_columns(df)
    else:
        print(df)
        raise RuntimeError('Dumbass fix this shit up frfr')
    df.drop(columns=('Game Info', "Rk"), axis=1, inplace=True)
    # reformats the results data which involves adding two columns (tm_points/opp_points) and cleaning an existing col
    results = list(df['Game Info']['Result'])
    result = []
    team_pts = []
    opp_team_pts = []
    total_team_pts = 0
    total_opp_pts = 0
    # when only 1 game is played df will not include season totals row which is expected in transforming / loading functions
    if len(results) == 1:
        df.loc[1] = df.loc[0].copy()
        df.loc[1, ('Game Info', 'Date')] = '1 Games'
    # loops through result column which is string, splits up the string and converst them to ints
    for i in range(0, len(df) - 1):
        result.append(results[i][0])
        team_pts.append(int(results[i][2:].split("-")[0]))
        total_team_pts += int(results[i][2:].split("-")[0])
        opp_team_pts.append(int(results[i][2:].split("-")[1]))
        total_opp_pts += int(results[i][2:].split("-")[1])
    # adds the record / total points scored to the end of the new columns
    result.append(results[len(results)-1])
    team_pts.append(total_team_pts)
    opp_team_pts.append(total_opp_pts)
    df.insert(loc=8, column=("Score","Tm"), value=team_pts)
    df.insert(loc=9, column=("Score", "Opp"), value=opp_team_pts)
    df.loc[:, ('Game Info', 'Result')] = result
    df.loc[:, ('Game Info', 'H/A')] = [0 if i == "@" else 1 for i in df['Game Info']['H/A']]

# saves player data into massive dataframe
def pull_position_data(player_links: dict) -> pd.DataFrame:
    """
        Takes player links, scrapes the current season data of that player, cleans, and combines those dataframes
        
        Args:
            player_links (dict): player_name: player_link (e.g "Lamar Jackson": "JackLa00")

        Returns:
            A combined dataframe of all individual player season stats, cleaned and ready to load into database 
    """
    position_df = pd.DataFrame()
    year = os.environ.get("NFL_SEASON")
    for player in player_links.values():
        url = "https://www.pro-football-reference.com/players/"+player[0]+"/"+player+"/gamelog/"+str(year)
        # 3 retries to load url
        for i in range(3):
            try:
                page = requests.get(url)
            except:
                if i < 3:
                    print("Retry attempt number: " + str(i+1))
                    time.sleep(3)
                    continue
                else:
                    raise RuntimeError("Could not request page: " + url)
            break
        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(3)
        table = soup.find("table")
        name = soup.find('div', {'id': 'meta'}).find('span').text
        try:
            pos = soup.find('div', {'id': 'meta'}).find(string='Position').next[2:4]
        except:
        # less relevant players may not have position listed, usually tightends, fullbacks, or lineman
            pos = "TE"
        # 3 retries for grabbing table
        for i in range(3):
            try:
                current_df = pd.read_html(io.StringIO(str(table)))[0]
            except:
                if i < 3:
                    print("Retry attempt number: " + str(i+1))
                    time.sleep(3)
                    continue
                else:
                    raise RuntimeError("Could not grab table from " + url)
            break
        try:
            clean_player_df(current_df)
            current_df[('Player Info', 'Name')] = name
            current_df[('Player Info', 'Pos')] = pos
            current_df[('Game Info', 'szn')] = year
            position_df = pd.concat([position_df, current_df])
        except:
            raise RuntimeError("Couldn't clean df: " + url)
    return position_df

def main() -> pd.DataFrame:
    links = pull_player_links()
    player_data = pull_position_data(links)
    player_data.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_data.csv")