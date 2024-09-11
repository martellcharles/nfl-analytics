"""
This module provides functions for uploading the transformed player average data to the database.
"""

import pandas as pd
import numpy as np
from nfl_stuff.helper_functions.databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os

def update_avg_team_stats(engine, session, df: pd.DataFrame) -> None:
    """
    Uploads the newest team average stats into the 'team_avg_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        team_df (pandas): df returned from create_team_avg_df()

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    team_avg_stats = pd.read_sql_query(session.query(TeamAvgStats).statement, engine)
    for idx in range(len(df)):
        game_id = df.loc[idx, 'game_id']
        team = df.loc[idx, 'team']
        curr_team = team_avg_stats.loc[(team_avg_stats['game_id'] == game_id) & (team_avg_stats['team'] == team), :]
        #team_avg_stats = pd.read_sql_query(session.query(TeamAvgStats).filter(TeamAvgStats.game_id==df.loc[idx, 'game_id'], 
        #                                                                      TeamAvgStats.team==df.loc[idx, 'team']).statement, engine)
        if len(curr_team) > 0:
            print(game_id + " + " + team + " combination already in database.")
            continue
        new_entry = TeamAvgStats(game_id=df.loc[idx, 'game_id'], szn=df.loc[idx, 'szn'], date=df.loc[idx, 'date'], 
                              team=df.loc[idx, 'team'], passing_cmp=df.loc[idx, 'passing_cmp'], 
                              passing_att=df.loc[idx, 'passing_att'], passing_cmp_prc=df.loc[idx, 'passing_cmp_prc'], 
                              passing_yds=df.loc[idx, 'passing_yds'], passing_tds=df.loc[idx, 'passing_tds'], 
                              passing_int=df.loc[idx, 'passing_int'], passing_rate=df.loc[idx, 'passing_rate'], 
                              passing_sacks=df.loc[idx, 'passing_sacks'], passing_sack_yds_lost=df.loc[idx, 'passing_sack_yds_lost'], 
                              passing_yds_att=df.loc[idx, 'passing_yds_att'], passing_net_yds_att=df.loc[idx, 'passing_net_yds_att'],
                              rushing_att=df.loc[idx, 'rushing_att'], rushing_yds=df.loc[idx, 'rushing_yds'], 
                              rushing_yds_att=df.loc[idx, 'rushing_yds_att'], rushing_tds=df.loc[idx, 'rushing_tds'], 
                              scoring_tds=df.loc[idx, 'scoring_tds'], scoring_pts=df.loc[idx, 'scoring_pts'], 
                              punts=df.loc[idx, 'punts'], punt_yds=df.loc[idx, 'punt_yds'], 
                              third_down_conv=df.loc[idx, 'third_down_conv'], fourth_down_conv=df.loc[idx, 'fourth_down_conv'])
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
    airflow_home = os.environ.get("AIRFLOW_HOME")
    # we do not calculate averages until week 2
    if not os.path.isfile(airflow_home + "/dags/nfl_stuff/data/team_avgs.csv"):
        return
    # load transformed data
    team_avg_stats = pd.read_csv(airflow_home + "/dags/nfl_stuff/data/team_avgs.csv")
    # Connect to database
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        update_avg_team_stats(engine, session, team_avg_stats)
    # clean up csvs to ensure dag doesn't use old data in next run
    os.remove(airflow_home + "/dags/nfl_stuff/data/team_avgs.csv")
    engine.dispose()