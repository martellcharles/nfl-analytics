"""
This module provides functions for uploading the cleaned team data to the database.
"""
import pandas as pd
import configparser
from databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os
    
def update_games(engine, session, df: pd.DataFrame, game_ids: dict) -> None:
    """
    Uploads the newest games into the 'games' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session, 
        games_df (pandas): df returned from clean_game()
        game_ids (dict): {game_string: game_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    games = pd.read_sql_query(session.query(Game).statement, engine)
    if len(games) == 0:
        curr_id = 1
    else:
        curr_id = max(games.loc[:,'game_id']) + 1
    for idx in range(len(df)):
        if 'Games' in df.loc[idx, ('Game Info', 'Date')]:
            continue
        if df.loc[idx, ('Game Info', 'H/A')] == 1:
            home = df.loc[idx, ('Game Info', 'Tm')]
            home_score = df.loc[idx, ('Score', 'Tm')]
            away = df.loc[idx, ('Game Info', 'Opp')]
            away_score = df.loc[idx, ('Score', 'Opp')]
        else:
            home = df.loc[idx, ('Game Info', 'Opp')]
            home_score = df.loc[idx, ('Score', 'Opp')]
            away = df.loc[idx, ('Game Info', 'Tm')]
            away_score = df.loc[idx, ('Score', 'Tm')]
        key = df.loc[idx, ('Game Info', 'Date')] + ' 00:00:00' + home + away
        if (game_ids.get(key) is None) and (not pd.isna(df.loc[idx, ('Score', 'Tm')])):
            new_entry = Game(game_id=curr_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], home_team=home, away_team=away, 
                            home_score=home_score, away_score=away_score, game_type='Regular')
            game_ids[key] = curr_id
            session.add(new_entry)
            curr_id += 1
    session.commit()
    game_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/game_ids.pkl"
    with open(game_ids_path, 'wb') as dickle:
        pickle.dump(game_ids, dickle)

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
    for idx in range(len(df)):
        if pd.isna(df.loc[idx, ('Score', 'Tm')]):
            continue
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
    
def update_id_dicts() -> None:
    """
        Updates the player_ids dict and game_ids dict, mostly used in development
    """
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    # Create the tables / session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    player_ids = {}
    game_ids = {}
    player_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_ids.pkl"
    game_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/game_ids.pkl"
    with Session() as session:
            players = pd.read_sql("SELECT * from players", engine)
            games = pd.read_sql("SELECT * from games", engine)
            for idx in range(len(players)):
                    player_ids[players.loc[idx, 'first_name'] + ' ' + players.loc[idx, 'last_name']] = players.loc[idx, 'player_id']
            for idx in range(len(games)):
                    game_ids[str(games.loc[idx, 'date']) + ' 00:00:00' + games.loc[idx, 'home_team'] + games.loc[idx, 'away_team']] = games.loc[idx, 'game_id']
            with open(player_ids_path, 'wb') as dickle:
                    pickle.dump(player_ids, dickle)
            with open(game_ids_path, 'wb') as dickle:
                    pickle.dump(game_ids, dickle)
    engine.dispose()
    
def main() -> None:
    """
    Uploads the latest week of game_stats into the all tables of the database.

    Args:
        Nothing, claned_team_data is loaded from csv saved to data folder

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    df = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/cleaned_team_data.csv")
    update_id_dicts()
    game_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/game_ids.pkl"
    with open(game_ids_path, 'rb') as dickle:
        game_ids = pickle.load(dickle)
    # Connect to database
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    # Create the tables / session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        update_games(engine, session, team_df, game_ids)
        with open(game_ids_path, 'rb') as dickle:
            game_ids = pickle.load(dickle)
        update_team_stats(engine, session, team_df, game_ids)
        update_avg_team_stats(engine, session, team_df)
    engine.dispose()