"""
This module provides functions for uploading the transformed player average data to the database.
"""

import pandas as pd
import numpy as np
from databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os

def update_avg_stats(engine, session, df: pd.DataFrame, table_name: str) -> None:
    """
    Uploads the players career/season averages up to this point in their career/season into the selected table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from calc_avg
        table_name (str): either 'career_avg_stats' or 'season_avg_stats'

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    if table_name == 'career_avg_stats':
        stats = pd.read_sql_query(session.query(CareerAvgStats).statement, engine)
    else:
        stats = pd.read_sql_query(session.query(SeasonAvgStats).statement, engine)
    for idx in range(len(df)):
        game_id = df.loc[idx, 'game_id']
        player_id = df.loc[idx, 'player_id']
        if len(stats.loc[(stats['game_id'] == game_id) & (stats['player_id'] == player_id),:]) > 0:
            continue
        if table_name == 'career_avg_stats':
            new_entry = CareerAvgStats(game_id=game_id, szn=df.loc[idx, 'szn'], date=df.loc[idx, 'date'], 
                              player_id=player_id, team=df.loc[idx, 'team'], 
                              passing_cmp=df.loc[idx, 'passing_cmp'], passing_att=df.loc[idx, 'passing_att'], 
                              passing_cmp_prc=df.loc[idx, 'passing_cmp_prc'], passing_yds=df.loc[idx, 'passing_yds'], 
                              passing_tds=df.loc[idx, 'passing_tds'], passing_int=df.loc[idx, 'passing_int'], 
                              passing_rate=df.loc[idx, 'passing_rate'], passing_sacks=df.loc[idx, 'passing_sacks'], 
                              passing_sack_yds_lost=df.loc[idx, 'passing_sack_yds_lost'], passing_yds_att=df.loc[idx, 'passing_yds_att'],
                              passing_adj_yds_att=df.loc[idx, 'passing_adj_yds_att'], rushing_att=df.loc[idx, 'rushing_att'],
                              rushing_yds=df.loc[idx, 'rushing_yds'], rushing_yds_att=df.loc[idx, 'rushing_yds_att'], 
                              rushing_tds=df.loc[idx, 'rushing_tds'], scoring_tds=df.loc[idx, 'scoring_tds'],
                              scoring_pts=df.loc[idx, 'scoring_pts'], receiving_rec=df.loc[idx, 'receiving_rec'],
                              receiving_yds=df.loc[idx, 'receiving_yds'], receiving_yds_rec=df.loc[idx, 'receiving_yds_rec'],
                              receiving_tds=df.loc[idx, 'receiving_tds'], receiving_tgts=df.loc[idx, 'receiving_tgts'],
                              receiving_catch_prc=df.loc[idx, 'receiving_catch_prc'], receiving_yds_tgt=df.loc[idx, 'receiving_yds_tgt'],
                              fumbles_fmb=df.loc[idx, 'fumbles_fmb'], fumbles_fl=df.loc[idx, 'fumbles_fl'])
        else:
            new_entry = SeasonAvgStats(game_id=game_id, szn=df.loc[idx, 'szn'], date=df.loc[idx, 'date'], 
                              player_id=player_id, team=df.loc[idx, 'team'], 
                              passing_cmp=df.loc[idx, 'passing_cmp'], passing_att=df.loc[idx, 'passing_att'], 
                              passing_cmp_prc=df.loc[idx, 'passing_cmp_prc'], passing_yds=df.loc[idx, 'passing_yds'], 
                              passing_tds=df.loc[idx, 'passing_tds'], passing_int=df.loc[idx, 'passing_int'], 
                              passing_rate=df.loc[idx, 'passing_rate'], passing_sacks=df.loc[idx, 'passing_sacks'], 
                              passing_sack_yds_lost=df.loc[idx, 'passing_sack_yds_lost'], passing_yds_att=df.loc[idx, 'passing_yds_att'],
                              passing_adj_yds_att=df.loc[idx, 'passing_adj_yds_att'], rushing_att=df.loc[idx, 'rushing_att'],
                              rushing_yds=df.loc[idx, 'rushing_yds'], rushing_yds_att=df.loc[idx, 'rushing_yds_att'], 
                              rushing_tds=df.loc[idx, 'rushing_tds'], scoring_tds=df.loc[idx, 'scoring_tds'],
                              scoring_pts=df.loc[idx, 'scoring_pts'], receiving_rec=df.loc[idx, 'receiving_rec'],
                              receiving_yds=df.loc[idx, 'receiving_yds'], receiving_yds_rec=df.loc[idx, 'receiving_yds_rec'],
                              receiving_tds=df.loc[idx, 'receiving_tds'], receiving_tgts=df.loc[idx, 'receiving_tgts'],
                              receiving_catch_prc=df.loc[idx, 'receiving_catch_prc'], receiving_yds_tgt=df.loc[idx, 'receiving_yds_tgt'],
                              fumbles_fmb=df.loc[idx, 'fumbles_fmb'], fumbles_fl=df.loc[idx, 'fumbles_fl'])
        session.add(new_entry)
    session.commit()

def update_career_totals(engine, session, df: pd.DataFrame) -> None:
    """
    Uploads the newest game stats into the 'game_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from calc_totals

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    career_totals = pd.read_sql_query(session.query(CareerTotals).statement, engine)
    for idx in range(len(df)):
        game_id = df.loc[idx, 'game_id']
        player_id = df.loc[idx, 'player_id']
        if len(career_totals.loc[(career_totals['game_id'] == game_id) & (career_totals['player_id'] == player_id), :]) > 0:
            continue
        new_entry = CareerTotals(game_id=game_id, szn=df.loc[idx, 'szn'], date=df.loc[idx, 'date'], 
                              player_id=player_id, team=df.loc[idx, 'team'], 
                              passing_cmp=df.loc[idx, 'passing_cmp'], passing_att=df.loc[idx, 'passing_att'], 
                              passing_cmp_prc=df.loc[idx, 'passing_cmp_prc'], passing_yds=df.loc[idx, 'passing_yds'], 
                              passing_tds=df.loc[idx, 'passing_tds'], passing_int=df.loc[idx, 'passing_int'], 
                              passing_rate=df.loc[idx, 'passing_rate'], passing_sacks=df.loc[idx, 'passing_sacks'], 
                              passing_sack_yds_lost=df.loc[idx, 'passing_sack_yds_lost'], passing_yds_att=df.loc[idx, 'passing_yds_att'],
                              passing_adj_yds_att=df.loc[idx, 'passing_adj_yds_att'], rushing_att=df.loc[idx, 'rushing_att'],
                              rushing_yds=df.loc[idx, 'rushing_yds'], rushing_yds_att=df.loc[idx, 'rushing_yds_att'], 
                              rushing_tds=df.loc[idx, 'rushing_tds'], scoring_tds=df.loc[idx, 'scoring_tds'],
                              scoring_pts=df.loc[idx, 'scoring_pts'], receiving_rec=df.loc[idx, 'receiving_rec'],
                              receiving_yds=df.loc[idx, 'receiving_yds'], receiving_yds_rec=df.loc[idx, 'receiving_yds_rec'],
                              receiving_tds=df.loc[idx, 'receiving_tds'], receiving_tgts=df.loc[idx, 'receiving_tgts'],
                              receiving_catch_prc=df.loc[idx, 'receiving_catch_prc'], receiving_yds_tgt=df.loc[idx, 'receiving_yds_tgt'],
                              fumbles_fmb=df.loc[idx, 'fumbles_fmb'], fumbles_fl=df.loc[idx, 'fumbles_fl'])
        session.add(new_entry)
    session.commit()
    
def main() -> None:
    """
    Uploads the latest week of player average stats into the averges tables of the database.

    Args:
        Nothing, dataframes are loaded from csvs saved to data folder

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    career_total_stats = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/career_totals.csv")
    career_avg_stats = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/career_avgs.csv")
    season_avg_stats = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/season_avgs.csv")
    # load current player ids
    curr_year_players_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/curr_year_players.pkl"
    with open(curr_year_players_path, 'rb') as dickle:
        player_ids = pickle.load(dickle)
    # Connect to database
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        update_career_totals(engine, session, career_total_stats)
        update_avg_stats(engine, session, career_avg_stats, 'career_avg_stats')
        update_avg_stats(engine, session, season_avg_stats, 'season_avg_stats')
    