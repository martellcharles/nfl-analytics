"""
This module provides functions for scraping the revelent data to add to database.
"""
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path
import io

# this dict of player links will be used to pull the player data, the dateframe contains 
def pull_player_links(statistic: str) -> dict:
    # loops through years and pulls the links of all players who have the requested stat as well as their season totals
    player_links = {}
    yearly_dfs = pd.DataFrame()
    for year in range(1970, 2024):
        # scrapes table from site and waits to ensure we don't send too many requests to the site
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + statistic + ".htm"
        try:
            page = requests.get(url)
        except:
            # f = open('./data/missed_players.txt', 'a')
            print(url)
            # f.write(url)
            # f.write('\n')
            # f.close()
            continue
        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(3)
        curr_year_links = []
        rows = soup.find("table").find("tbody").find_all("tr")
        # this table contains the season totals for every player we gather, saving us some calculation later
        df = pd.read_html(io.StringIO(str(soup.find("table"))))[0]
        df = clean_season_df(df, df.columns.nlevels==2, statistic.title(), year)
        # assigns variables needed for loop to function
        for idx, row in enumerate(rows):
            # grabs element of row that contains the player link
            grandchildren = list(list(row.children)[1].children)
            # sometimes has non-qb stats or rows that show column names
            if df.loc[idx, ('Game Info', 'Pos')] == 'Pos':
                continue
            else:
                curr_year_links.append(grandchildren[0]['href'])
        player_links[year] = curr_year_links    
        yearly_dfs = pd.concat([yearly_dfs, df])
    return player_links, yearly_dfs

def clean_season_df(df: pd.DataFrame, levels: bool, statistic: str, year: int) -> pd.DataFrame:
    if levels:
        df = fix_double_level_columns(df)
    else:
        new_col_level = ['Game Info' if i < 5 else 'Games' if i < 7 else statistic for i in range(len(df.columns))]
        df.columns = [new_col_level, df.columns]
    df.loc[:,('Game Info','Rk')] = year
    df.rename(columns={'Rk': 'szn'}, level=1, inplace=True)
    return df

# if table is scraped with multi column indices, this code cleans up the column names who were scraped weird
def fix_double_level_columns(df: pd.DataFrame) -> pd.DataFrame:
    col1 = {}
    col2 = {}
    for i in df.columns:
        if "Unnamed:" in i[0]:
            col1[i[0]] = 'Game Info'
        if "Unnamed:" in i[1]:
            col2[i[1]] = 'H/A'
    df.rename(columns=col1, level=0, inplace=True)
    df.rename(columns=col2, level=1, inplace=True)
    return df

def clean_player_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.columns.nlevels == 2:
        df = fix_double_level_columns(df)
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
    # loops through result column which is string, splits up the string and converst them to ints
    for i in range(0, len(results) - 1):
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
    return df

# saves player data into massive dataframe
def pull_position_data(player_links: dict) -> pd.DataFrame:
    position_df = pd.DataFrame()
    for year in player_links.keys():
        for player in player_links.get(year):
            url = "https://www.pro-football-reference.com/"+player[:-4]+"/gamelog/"+str(year)
            try:
                page = requests.get(url)
            except:
                # f = open('./data/missed_players.txt', 'a')
                print(url)
                # f.write(url)
                # f.write('\n')
                # f.close()
                continue
            soup = BeautifulSoup(page.content, "html.parser")
            time.sleep(3)
            table = soup.find("table")
            try:
                name = soup.find('div', {'id': 'meta'}).find('span').text
                pos = soup.find('div', {'id': 'meta'}).find(text='Position').next[2:4]
            except:
                pos = "TE"
            try:
                current_df = pd.read_html(io.StringIO(str(table)))[0]
                current_df = clean_player_df(current_df)
                current_df[('Player Info', 'Name')] = name
                current_df[('Player Info', 'Pos')] = pos
                current_df[('Game Info', 'szn')] = year
                position_df = pd.concat([position_df, current_df])
                # position_df.to_csv('./data/current_players.csv', index=False)
            except:
                # f = open('./data/missed_players.txt', 'a')
                print(url)
                # f.write(url)
                # f.write('\n')
                # f.close()
                continue
    return position_df

def save_all_player_data() -> None:
    # currently scraping players data several times per year
    # need to fix this to cut down on ~2 day runtime
    passing_links, passing_yearly_dfs = pull_player_links('passing')
    passing_df = pull_position_data(passing_links)
    rushing_links, rushing_yearly_dfs = pull_player_links('rushing')
    rushing_df = pull_position_data(rushing_links)
    receiving_links, receiving_yearly_dfs = pull_player_links('receiving')
    receiving_df = pull_position_data(receiving_links)
    all_games = pd.concat([passing_df, rushing_df, receiving_df])
    all_seasons = pd.concat([passing_yearly_dfs, rushing_yearly_dfs, receiving_yearly_dfs])
    all_games.to_csv('./data/all_games.csv', index=False)
    all_seasons.to_csv('./data/all_seasons.csv', index=False)

def save_defensive_player_data() -> None:
    defensive_links, yearly_defensive_dfs = pull_player_links('defense')
    defense_df = pull_position_data(defensive_links)
    yearly_defensive_dfs.to_csv('./data/defense_szns.csv', index=False)
    defense_df.to_csv('./data/defense_df.csv', index=False)

# saves team data into 53 year directories with around 26-32 teams in each depending on the year
def pull_team_data() -> None:
    # teams in 1995
    teams = ['crd', 'atl', 'buf', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'clt', 'kan', 'rai', 'sea', 'tam',
            'car', 'jax', 'sdg', 'ram', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sfo', 'oti', 'was']
    for year in range(1970, 2023):
        print(year)
        #adding teams to list as they join the nfl
        if year == 1976:
            teams.append('sea')
            teams.append('tam')
        elif year == 1995:
            teams.append('car')
            teams.append('jax')
        elif year == 1996:
            teams.append('rav')
        elif year == 2002:
            teams.append('htx')
        for team in teams:
            url = "https://www.pro-football-reference.com/teams/" + team + "/" + str(year) + "/gamelog/"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            time.sleep(3.5)
            try:
                string = "gamelog_opp" + str(year)
                table = soup.find("table", {"id": string})
                df = pd.read_html(str(table))[0]
            except:
                # cleveland didn't have a team for a few years so this accounts for those seasons
                print(team + " did not exist in " + str(year))
                continue
            # cleaning data
            col1 = {}
            col2 = {}
            df.drop(columns=("Unnamed: 3_level_0", "Unnamed: 3_level_1"), axis=1, inplace=True)
            df.rename(columns={"Unnamed: 4_level_1": "Result"}, level=1, inplace=True)
            for i in df.columns:
                if "Unnamed:" in i[0]:
                    col1[i[0]] = 'Game Info'
                if "Unnamed:" in i[1]:
                    col2[i[1]] = 'H/A'
            df.rename(columns=col1, level=0, inplace=True)
            df.rename(columns=col2, level=1, inplace=True)
            df.loc[:, ('Game Info', 'H/A')] = [0 if i == "@" else 1 for i in df['Game Info']['H/A']]
            df.loc[:, ('Game Info', 'OT')] = [int(0) if pd.isnull(i) else int(1) for i in df['Game Info']['OT']]
            months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 
                'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
            df.loc[:, ('Game Info', 'Date')] = [str(year) + '-' + str(months_dict.get(i.split(" ")[0])) + '-' + i.split(" ")[1] for i in df['Game Info']['Date']]
            # creates new directory if it doesn't exist
            file = team + ".csv"
            directory = Path("./team_data/original_data/" + str(year) + "/")
            directory.mkdir(parents=True, exist_ok=True)
            df.to_csv(directory / file, index=False)

# scrape team defensive data with year specified in the function
def scrape_team_data() -> pd.DataFrame:
    year = 2024
    teams = ['crd', 'atl', 'buf', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'clt', 'kan', 'rai', 'sea', 'tam', 'rav',
            'car', 'jax', 'sdg', 'ram', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sfo', 'oti', 'was', 'htx']
    all_teams = pd.DataFrame()
    for team in teams:
        url = "https://www.pro-football-reference.com/teams/" + team + "/" + str(year) + "/gamelog/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(3)
        try:
            string = "gamelog_opp" + str(year)
            table = soup.find("table", {"id": string})
            df = pd.read_html(io.StringIO(str(table)))[0]
        except:
            print(url)
            raise RuntimeError("What the fuck")
        # cleaning data
        col1 = {}
        col2 = {}
        df.drop(columns=("Unnamed: 3_level_0", "Unnamed: 3_level_1"), axis=1, inplace=True)
        df.rename(columns={"Unnamed: 4_level_1": "Result"}, level=1, inplace=True)
        for i in df.columns:
            if "Unnamed:" in i[0]:
                col1[i[0]] = 'Game Info'
            if "Unnamed:" in i[1]:
                col2[i[1]] = 'H/A'
        df.rename(columns=col1, level=0, inplace=True)
        df.rename(columns=col2, level=1, inplace=True)
        df.loc[:, ('Game Info', 'H/A')] = [0 if i == "@" else 1 for i in df['Game Info']['H/A']]
        df.loc[:, ('Game Info', 'OT')] = [int(0) if pd.isnull(i) else int(1) for i in df['Game Info']['OT']]
        df[('Game Info', 'Tm')] = team
        df[('Game Info', 'szn')] = year
        months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 
            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        df.loc[:, ('Game Info', 'Date')] = [str(year+1) + '-' + str(months_dict.get(i.split(" ")[0])) + '-' + i.split(" ")[1] if months_dict.get(i.split(" ")[0])<3 else str(year) + '-' + str(months_dict.get(i.split(" ")[0])) + '-' + i.split(" ")[1] for i in df['Game Info']['Date']]
        all_teams = pd.concat([all_teams, df])
    all_teams.reset_index(drop=True, inplace=True)
    return all_teams


def main() -> pd.DataFrame:
    passing_links, passing_yearly_dfs = pull_player_links('passing')
    passing_df = pull_position_data(passing_links)
    rushing_links, rushing_yearly_dfs = pull_player_links('rushing')
    rushing_df = pull_position_data(rushing_links)
    receiving_links, receiving_yearly_dfs = pull_player_links('receiving')
    receiving_df = pull_position_data(receiving_links)
    all_games = pd.concat([passing_df, rushing_df, receiving_df])
    # now calculating season data from games data
    #all_seasons = pd.concat([passing_yearly_dfs, rushing_yearly_dfs, receiving_yearly_dfs])
    all_teams = scrape_team_data()
    return all_games, all_teams