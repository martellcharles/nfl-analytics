"""
This module provides functions for cleaning the scraped player data to prepare for database entry.
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle
import os

Base = declarative_base()


def fix_snap_cols(df: pd.DataFrame, col_names: list) -> None:
    """
    Fixes the columns that track the snap num/percentage stats.

    Args:
        games_df (pandas df): dataframe of stats per player per game.
        col_names (list): Dataframe of stats per player per game as well as snap columns to be fixed.

    Returns:
        Nothing, the dataframe is edited in place and is called in the clean_games function. 
    """
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

# occasionally a player will have two rows of data for the same week, we need to make changes to this function to
# ensure that we clean those up

def clean_games(df: pd.DataFrame) -> None:
    """
    Further cleans the dataframe of game stats to match database format.

    Args:
        games_df (pandas): Dataframe of stats per player per game.

    Returns:
        Nothing, the dataframe is edited in place.. 
    """
    df.loc[:,('Game Info','Tm')] = [team.lower() if type(team)==str else np.nan for team in df['Game Info']['Tm']]
    df.loc[:,('Game Info','Opp')] = [opp.lower() if type(opp)==str else np.nan for opp in df['Game Info']['Opp']]
    for stat in ['Passing', 'Rushing', 'Receiving', 'Fumbles', 'Scoring']:
        for col in df[stat].columns:
            df[(stat,col)] = pd.to_numeric(df[(stat,col)], errors='coerce')
    df.reset_index(drop=True, inplace=True)
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
    df.fillna(0, inplace=True)

def main() -> pd.DataFrame:
    player_data = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_data.csv")
    clean_games(player_data)
    player_data.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/cleaned_player_data.csv")