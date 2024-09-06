"""
This module provides functions for uploading the cleaned team data to the database.
"""
import pandas as pd
import configparser
from sources.dags.databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle

def update_team_stats(engine, session, df: pd.DataFrame, game_ids: dict):
    """
    Uploads the newest team stats into the 'team_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        team_df (pandas): df returned from clean_team_df(), 
        game_ids: {game_string: game_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    team_stats = pd.read_sql_query(session.query(TeamStats).filter(TeamStats.szn==df.loc[0, ('Game Info', 'szn')]).statement, engine)
    #team_stats = pd.read_sql("SELECT * from team_stats where szn="+str(df.loc[0, ('Game Info', 'szn')]), engine)
    for idx in range(len(df)):
        if df.loc[idx, ('Game Info', 'H/A')] == 1:
            home = df.loc[idx, ('Game Info', 'Tm')]
            away = df.loc[idx, ('Game Info', 'Opp')]
        else:
            home = df.loc[idx, ('Game Info', 'Opp')]
            away = df.loc[idx, ('Game Info', 'Tm')]
        key = df.loc[idx, ('Game Info', 'Date')] + ' 00:00:00' + home + away
        game_id = game_ids.get(key)
        if game_id is None:
            raise RuntimeError("game_id not found: " + key)
        if len(team_stats.loc[(team_stats['game_id'] == game_id) & (team_stats['team']==df.loc[idx, ('Game Info', 'Tm')]), :]) > 0:
            continue
        total_tds = df.loc[idx, ('Passing', 'TD')] + df.loc[idx, ('Rushing', 'TD')]
        total_pts = (total_tds*6) + (df.loc[idx, ('Scoring', 'FGM')]*3) + df.loc[idx, ('Scoring', 'XPM')]
        new_entry = TeamStats(game_id=game_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], 
                              team=df.loc[idx, ('Game Info', 'Tm')], passing_cmp=df.loc[idx, ('Passing', 'Cmp')], 
                              passing_att=df.loc[idx, ('Passing', 'Att')], passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], 
                              passing_yds=df.loc[idx, ('Passing', 'Yds')], passing_tds=df.loc[idx, ('Passing', 'TD')], 
                              passing_int=df.loc[idx, ('Passing', 'Int')], passing_rate=df.loc[idx, ('Passing', 'Rate')], 
                              passing_sacks=df.loc[idx, ('Passing', 'Sk')], passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], 
                              passing_yds_att=df.loc[idx, ('Passing', 'Y/A')], passing_net_yds_att=df.loc[idx, ('Passing', 'NY/A')],
                              rushing_att=df.loc[idx, ('Rushing', 'Att')], rushing_yds=df.loc[idx, ('Rushing', 'Yds')], 
                              rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], rushing_tds=df.loc[idx, ('Rushing', 'TD')], 
                              scoring_tds=total_tds, scoring_pts=total_pts, 
                              punts=df.loc[idx, ('Punting', 'Pnt')], punt_yds=df.loc[idx, ('Punting', 'Yds')], 
                              third_down_conv=df.loc[idx, ('Downs', '3DConv')], third_down_att=df.loc[idx, ('Downs', '3DAtt')], 
                              fourth_down_conv=df.loc[idx, ('Downs', '4DConv')], fourth_down_att=df.loc[idx, ('Downs', '4DAtt')])
        session.add(new_entry)
    session.commit()


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
    
def main(df: pd.DataFrame, team_df: pd.DataFrame) -> None:
    """
    Uploads the latest week of game_stats into the all tables of the database.

    Args:
        games_df (pandas): Cleaned dataframe of stats per player per game
        team_df (pandas): cleaned dataframe of team defensive stats per game.
        game_ids (dict): {game_string: game_id}
        player_ids (dict): {player name: player_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    with open('./data/game_ids.pkl', 'rb') as dickle:
        game_ids = pickle.load(dickle)
    # Connect to database
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    user = config['DATABASE']['user']
    password = config['DATABASE']['password']
    server = config['DATABASE']['host']
    db = config['DATABASE']['db_dev']
    engine = create_engine(f"mysql+mysqldb://{user}:{password}@{server}/{db}")
    # Create the tables / session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        update_team_stats(engine, session, team_df, game_ids)
        update_avg_team_stats(engine, session, team_df)
    engine.dispose()