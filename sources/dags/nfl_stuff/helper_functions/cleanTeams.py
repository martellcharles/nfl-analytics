"""
This module provides functions for cleaning the scraped team data to prepare for database entry.
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle
import os

Base = declarative_base()

def clean_team_df(df: pd.DataFrame) -> None:
    """
    Cleans the dataframe of team stats to match database format.

    Args:
        df (pandas): Dataframe of team stats per game per team.

    Returns:
        Nothing, the dataframe is edited in place.. 
    """
    df.fillna(0, inplace=True)
    drop = []
    for idx in range(len(df)):
        # extractTeams() scrapes all weeks that have not been played yet, this drops those weeks
        # assumes no game will ever end 0-0, which is possible but incredibly unlikely
        if (df.loc[idx, ('Score', 'Tm')] == 0) and (df.loc[idx, ('Score', 'Opp')] == 0):
            drop.append(idx)
            continue
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
    df.drop(drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/cleaned_team_data.csv", index=False)
    
def main() -> pd.DataFrame:
    team_data = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/team_data.csv", header=[0,1])
    clean_team_df(team_data)