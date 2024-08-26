"""
This module provides functions for cleaning the scraped data to prepare for database entry.
"""
import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle

Base = declarative_base()


def fix_snap_cols(df: pd.DataFrame, col_names: list) -> None:
    for tup in col_names:
        if tup[1] == 'Num':
            for idx in range(len(df)):
                try:
                    df.loc[idx, tup] = float(df.loc[idx, tup])
                except:
                    df.loc[idx, tup] = np.nan
        else:
            for idx in range(len(df)):
                if pd.isna(df.loc[idx, tup]):
                    continue
                if df.loc[idx, tup][-1] == '%':
                    df.loc[idx, tup] = float(df.loc[idx, tup][:-1]) / 100
                else:
                    df.loc[idx, tup] = np.nan

def clean_games(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe of game stats scraped from pro-football-reference.com.

    Args:
        games_df (pandas): Dataframe of stats per player per game.

    Returns:
        Nothing, the dataframe is edited in place and saves dataframe in local directory as 'games.csv'. 
    """
    df.loc[:,('Game Info','Tm')] = [team.lower() if type(team)==str else np.nan for team in df['Game Info']['Tm']]
    df.loc[:,('Game Info','Opp')] = [opp.lower() if type(opp)==str else np.nan for opp in df['Game Info']['Opp']]
    for stat in ['Passing', 'Rushing', 'Receiving', 'Fumbles', 'Scoring']:
        for col in df[stat].columns:
            df[(stat,col)] = pd.to_numeric(df[(stat,col)], errors='coerce')
    fix_snap_cols(df, [('Off. Snaps', 'Num'), ('Off. Snaps', 'Pct'), ('ST Snaps', 'Num'), ('ST Snaps', 'Pct'), 
                       ('Def. Snaps', 'Num'), ('Def. Snaps', 'Pct')])
    drop = []
    for idx in range(1,len(df)):
        if df.loc[idx, ('Game Info', 'Week')] == df.loc[idx-1,('Game Info', 'Week')]:
            drop.append(idx)
    df.drop(drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    for player in df[('Player Info', 'Name')].unique():
        indices = df.loc[df[('Player Info', 'Name')] == player,:].index
        drop = []
        for i,idx in enumerate(indices):
            if 'Games' in df.loc[idx,('Game Info', 'Date')]:
                i+=1
                drop = [j for j in indices[i:]]
                break
            elif df.loc[idx, ('Game Info', 'Week')] == df.loc[indices[i-1],('Game Info', 'Week')] and len(indices) > 1:
                drop = [indices[i-1]]
                break
        try:
            df.drop(drop, inplace=True)
            df.reset_index(drop=True, inplace=True)
        except:
            raise RuntimeError(player + " failed!")
    # df.drop(drop, inplace=True)
    # df.reset_index(drop=True, inplace=True)
    return df

def clean_team_df(df: pd.DataFrame) -> None:
    for idx in range(len(df)):
        # adds 0s to single digit months and days to match formatting for game_id key
        if len(df.loc[idx, ('Game Info', 'Date')].split('-')[1]) == 1:
            df.loc[idx, ('Game Info', 'Date')] = df.loc[idx, ('Game Info', 'Date')].split('-')[0] + '-0' + df.loc[idx, ('Game Info', 'Date')].split('-')[1] + '-' + df.loc[idx, ('Game Info', 'Date')].split('-')[2]
        if len(df.loc[idx, ('Game Info', 'Date')].split('-')[2]) == 1:
            df.loc[idx, ('Game Info', 'Date')] = df.loc[idx, ('Game Info', 'Date')].split('-')[0] + '-' + df.loc[idx, ('Game Info', 'Date')].split('-')[1] + '-0' + df.loc[idx, ('Game Info', 'Date')].split('-')[2]
        # changes team column to match formatting of database. there are 32 urls for each team, but in the database there are 39 possible team abbreviations.
        # this is because when teams change city their abbrevation changes, e.g. the raiders moved from oakland to LA back to oakland and finally to las vegas
        if df.loc[idx, ('Game Info', 'Tm')] == 'rai':
            if df.loc[idx, ('Game Info', 'szn')] < 1982:
                df.loc[idx, ('Game Info', 'Tm')] = 'oak'
            elif df.loc[idx, ('Game Info', 'szn')] < 1995:
                df.loc[idx, ('Game Info', 'Tm')] = 'rai'
            elif df.loc[idx, ('Game Info', 'szn')] < 2020:
                df.loc[idx, ('Game Info', 'Tm')] = 'oak'
            else:
                df.loc[idx, ('Game Info', 'Tm')] = 'lvr'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'htx':
            df.loc[idx, ('Game Info', 'Tm')] = 'hou'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'rav':
            df.loc[idx, ('Game Info', 'Tm')] = 'bal'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'sdg' and df.loc[idx, ('Game Info', 'szn')] > 2016:
            df.loc[idx, ('Game Info', 'Tm')] = 'lac'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'crd':
            if df.loc[idx, ('Game Info', 'szn')] < 1988:
                df.loc[idx, ('Game Info', 'Tm')] = 'stl'
            elif df.loc[idx, ('Game Info', 'szn')] < 1994:
                df.loc[idx, ('Game Info', 'Tm')] = 'pho'
            else:
                df.loc[idx, ('Game Info', 'Tm')] = 'ari'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'nwe' and df.loc[idx, ('Game Info', 'szn')] == 1970:
            df.loc[idx, ('Game Info', 'Tm')] = 'bos'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'oti':
            if df.loc[idx, ('Game Info', 'szn')] < 1997:
                df.loc[idx, ('Game Info', 'Tm')] = 'hou'
            else:
                df.loc[idx, ('Game Info', 'Tm')] = 'ten'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'ram':
            if df.loc[idx, ('Game Info', 'szn')] < 1995:
                continue
            elif df.loc[idx, ('Game Info', 'szn')] < 2016:
                df.loc[idx, ('Game Info', 'Tm')] = 'stl'
            else:
                df.loc[idx, ('Game Info', 'Tm')] = 'lar'
        elif df.loc[idx, ('Game Info', 'Tm')] == 'clt':
            if df.loc[idx, ('Game Info', 'szn')] < 1984:
                df.loc[idx, ('Game Info', 'Tm')] = 'bal'
            else:
                df.loc[idx, ('Game Info', 'Tm')] = 'ind'
        # this change is needed because the original LA rams used abbreviation ram whereas current LA rams use lar
        if df.loc[idx, ('Game Info', 'Opp')] == 'Los Angeles Rams' and df.loc[idx, ('Game Info', 'szn')] < 1995:
            df.loc[idx, ('Game Info', 'Opp')] = 'Los Angeles Rams1'
        # this dict is used to convert full team name to appropriate abbreviation
        teams_dict = {'New Orleans Saints': 'nor', 'Green Bay Packers': 'gnb', 'San Francisco 49ers': 'sfo', 'Dallas Cowboys': 'dal', 'Denver Broncos': 'den',
            'Chicago Bears': 'chi', 'Los Angeles Rams': 'lar', 'Philadelphia Eagles': 'phi', 'Miami Dolphins': 'mia', 'Pittsburgh Steelers': 'pit',
            'Minnesota Vikings': 'min', 'New York Jets': 'nyj', 'Boston Patriots': 'bos', 'Cincinnati Bengals': 'cin', 'Baltimore Colts': 'bal',
            'New York Giants': 'nyg', 'Detroit Lions': 'det', 'San Diego Chargers': 'sdg', 'Atlanta Falcons': 'atl', 'Buffalo Bills': 'buf', 
            'Oakland Raiders': 'oak', 'Houston Oilers': 'hou', 'Cleveland Browns': 'cle', 'Kansas City Chiefs': 'kan', 'Washington Redskins': 'was',
            'St. Louis Cardinals': 'stl', 'New England Patriots': 'nwe', 'Seattle Seahawks': 'sea', 'Tampa Bay Buccaneers': 'tam', 
            'Los Angeles Raiders': 'rai', 'Indianapolis Colts': 'ind', 'Phoenix Cardinals': 'pho', 'Arizona Cardinals': 'ari', 'Carolina Panthers': 'car',
            'St. Louis Rams': 'stl', 'Jacksonville Jaguars': 'jax', 'Baltimore Ravens': 'bal', 'Tennessee Oilers': 'ten', 'Tennessee Titans': 'ten', 
            'Houston Texans': 'hou', 'Los Angeles Chargers': 'lac', 'Las Vegas Raiders': 'lvr', 'Washington Football Team': 'was', 
            'Washington Commanders': 'was', 'Los Angeles Rams1': 'ram'}
        df.loc[idx, ('Game Info', 'Opp')] = teams_dict.get(df.loc[idx, ('Game Info', 'Opp')])
    df = df.replace({np.nan: None})

def clean_season(df: pd.DataFrame) -> None:
    drop = []
    for idx, row in df.iterrows():
        if idx in drop:
            continue
        if 'Player' in row.iloc[1]:
            drop.append(idx)
            continue
        if len(df.loc[df[('Game Info', 'Player')] == row.iloc[1],:]) > 1:
               indices = df.loc[df[('Game Info', 'Player')] == row.iloc[1], :].index
               for i in range(1,len(df.loc[df[('Game Info', 'Player')] == row.iloc[1],:])):
                   drop.append(indices[i])
                   for j in range(6,len(df.columns)):
                       if pd.isna(df.iloc[indices[0],j]) and not pd.isna(df.iloc[indices[i],j]):
                            df.iloc[indices[0],j] = df.iloc[indices[i],j]
        if '+' in row.iloc[1]:
            df.iloc[idx, 1] = df.iloc[idx, 1][:-1]
        if '*' in row.iloc[1]:
            df.iloc[idx, 1] = df.iloc[idx, 1][:-1]
    df.drop(drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.loc[:,('Game Info','Tm')]= [team.lower() for team in df['Game Info']['Tm']]
    df.to_csv('curr_season_szn.csv', index=False)

def update_id_dicts() -> None:
    """
        Updates the player_ids dict and game_ids dict, mostly used in development
    """
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    user = config['DATABASE']['user']
    password = config['DATABASE']['password']
    server = config['DATABASE']['host']
    db = config['DATABASE']['db_dev']
    ssl = config['DATABASE']['ssl_ca']
    engine = create_engine(f"mysql+mysqldb://{user}:{password}@{server}/{db}?ssl_ca={ssl}")
    # Create the tables / session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    player_ids = {}
    game_ids = {}
    with Session() as session:
            players = pd.read_sql("SELECT * from players", engine)
            games = pd.read_sql("SELECT * from games", engine)
            for idx in range(len(players)):
                    player_ids[players.loc[idx, 'first_name'] + ' ' + players.loc[idx, 'last_name']] = players.loc[idx, 'player_id']
            for idx in range(len(games)):
                    game_ids[str(games.loc[idx, 'date']) + games.loc[idx, 'home_team'] + games.loc[idx, 'away_team']] = games.loc[idx, 'game_id']
            with open('./data/player_ids.pkl', 'wb') as dickle:
                    pickle.dump(player_ids, dickle)
            with open('./data/game_ids.pkl', 'wb') as dickle:
                    pickle.dump(game_ids, dickle)
    engine.dispose()

def main(games_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    update_id_dicts()
    cleaned_games = clean_games(games_df)
    cleaned_teams = clean_team_df(teams_df)
    return cleaned_games, cleaned_teams