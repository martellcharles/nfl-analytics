"""
This module provides functions for uploading the cleaned player data to the database.
"""

import pandas as pd
import numpy as np
import configparser
from databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os

def update_players(engine, session, df: pd.DataFrame, player_ids: dict) -> None:
    """
    Uploads the newest players into the 'players' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session, 
        games_df (pandas): df returned from clean_games()
        player_ids (dict): {player_name: player_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    players = pd.read_sql_query(session.query(Player).statement, engine)
    if len(players) == 0:
        curr_id = 1
    else:
        curr_id = players.iloc[-1,0] + 1
    for player in df[('Player Info', 'Name')].unique():
        first_name = player.split(' ',1)[0]
        last_name = player.split(' ',1)[1]
        if player_ids.get(first_name + ' ' + last_name):
            player_id = player_ids.get(first_name + ' ' + last_name)
            update = session.query(Player).filter_by(player_id=player_id).one()
            update.last_year = df.loc[df[('Player Info', 'Name')] == player, ('Game Info', 'szn')].iloc[0]
        else:
            position = df.loc[df[('Player Info', 'Name')] == player, ('Player Info', 'Pos')].iloc[0]
            first_year = df.loc[df[('Player Info', 'Name')] == player, ('Game Info', 'szn')].iloc[0]
            new_entry = Player(player_id=curr_id, first_name=first_name, last_name=last_name, position=position, first_year=first_year, last_year=first_year)
            player_ids[first_name + ' ' + last_name] = curr_id
            curr_id += 1
            session.add(new_entry)
    session.commit()
    player_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_ids.pkl"
    with open(player_ids_path, 'wb') as dickle:
        pickle.dump(player_ids, dickle)

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
    #games = pd.read_sql("SELECT * from games", engine)
    if len(games) == 0:
        curr_id = 1
    else:
        curr_id = games.iloc[-1,0] + 1
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
        if game_ids.get(key) is None:
            new_entry = Game(game_id=curr_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], home_team=home, away_team=away, 
                            home_score=home_score, away_score=away_score, game_type='Regular')
            game_ids[key] = curr_id
            session.add(new_entry)
            curr_id += 1
    session.commit()
    game_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/game_ids.pkl"
    with open(game_ids_path, 'wb') as dickle:
        pickle.dump(game_ids, dickle)


def update_game_stats(session, df: pd.DataFrame, game_ids: dict, player_ids: dict) -> None:
    """
    Uploads the newest game stats into the 'game_stats' table of the database.

    Args:
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from clean_game() 
        game_ids (dict): {game_string: game_id}
        player_ids (dict): {player_name: player_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    for idx in range(len(df)):
        if 'Games' in df.loc[idx, ('Game Info', 'Date')]:
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
            print(key)
            break
        player_id = player_ids.get(df.loc[idx, ('Player Info', 'Name')])
        new_entry = GameStats(game_id=game_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], 
                              player_id=player_id, team=df.loc[idx, ('Game Info', 'Tm')], 
                              passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                              passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                              passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                              passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                              passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                              passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                              rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                              rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                              scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                              receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                              receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                              receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                              fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')],
                              off_snap_num=df.loc[idx, ('Off. Snaps', 'Num')], off_snap_prc=df.loc[idx, ('Off. Snaps', 'Pct')],
                              st_snap_num=df.loc[idx, ('ST Snaps', 'Num')], st_snap_prc=df.loc[idx, ('ST Snaps', 'Pct')])
        session.add(new_entry)
    session.commit()


def update_season_stats(engine, session, df: pd.DataFrame, player_ids: dict) -> None:
    """
    Uploads / updates the newest season stats into the 'season_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from clean_game()
        player_ids (dict): {player_name: player_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    all_szn_stats = pd.read_sql_query(session.query(SeasonStats).statement, engine)
    for player in df[('Player Info', 'Name')].unique():
        player_id = player_ids.get(player)
        idx = df.loc[df[('Player Info', 'Name')]==player,:].index[-1]
        if 'Games' not in df.loc[idx, ('Game Info', 'Date')]:
            gp = len(df.loc[df[('Player Info', 'Name')]==player,:]) - 1
        else:
            gp = int(df.loc[idx, ('Game Info', 'Date')].split(' ')[0])
        team = df.loc[df[('Player Info', 'Name')]==player,('Game Info', 'Tm')].iloc[0]
        szn = df.loc[idx, ('Game Info', 'szn')]
        szn_stats = all_szn_stats.loc[(all_szn_stats['szn'] == szn) & (all_szn_stats['player_id'] == str(player_id)), :]
        if len(szn_stats) == 0:
            new_entry = SeasonStats(player_id=player_id, szn=szn, 
                                    player_name=player, team=team, games_played=gp,
                                    passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                                    passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                                    passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                                    passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                                    passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                                    passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                                    rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                                    rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                                    scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                                    receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                                    receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                                    receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                                    fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')])
            session.add(new_entry)
        else:
            update = session.query(SeasonStats).filter_by(id=player_id, szn=df.loc[idx, ('Game Info', 'szn')]).one()
            update.team=team
            update.games_played=gp
            update.passing_cmp=df.loc[idx, ('Passing', 'Cmp')]
            update.passing_att=df.loc[idx, ('Passing', 'Att')]
            update.passing_cmp=df.loc[idx, ('Passing', 'Cmp%')]
            update.passing_yds=df.loc[idx, ('Passing', 'Yds')]
            update.passing_tds=df.loc[idx, ('Passing', 'TD')]
            update.passing_int=df.loc[idx, ('Passing', 'Int')]
            update.passing_rate=df.loc[idx, ('Passing', 'Rate')]
            update.passing_sacks=df.loc[idx, ('Passing', 'Sk')]
            update.passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')]
            update.passing_yds_att=df.loc[idx, ('Passing', 'Y/A')]
            update.passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')]
            update.rushing_att=df.loc[idx, ('Rushing', 'Att')]
            update.rushing_yds=df.loc[idx, ('Rushing', 'Yds')]
            update.rushing_tds=df.loc[idx, ('Rushing', 'TD')]
            update.rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')]
            update.scoring_tds=df.loc[idx, ('Scoring', 'TD')]
            update.scoring_pts=df.loc[idx, ('Scoring', 'Pts')]
            update.receiving_rec=df.loc[idx, ('Receiving', 'Rec')]
            update.receiving_yds=df.loc[idx, ('Receiving', 'Yds')]
            update.receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')]
            update.receiving_tds=df.loc[idx, ('Receiving', 'TD')]
            update.receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')]
            update.receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')]
            update.receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')]
            update.fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')]
            update.fumbles_fl=df.loc[idx, ('Fumbles', 'FL')]
    session.commit()

def update_career_stats(engine, session, df: pd.DataFrame, player_ids: dict) -> None:
    """
    Uploads / updates the newest stats into the 'career_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session, 
        games_df (pandas): df returned from clean_game()
        player_ids (dict): {player_name: player_id}

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    career_stats = pd.read_sql_query(session.query(CareerStats).statement, engine)
    for player in df[('Player Info', 'Name')].unique():
        player_id = player_ids.get(player)
        player_stats = career_stats.loc[career_stats['player_id']==player_id,:]
        idx = df.loc[df[('Player Info', 'Name')]==player,:].index[-1]
        if 'Games' not in df.loc[idx, ('Game Info', 'Date')]:
            gp = len(df.loc[df[('Player Info', 'Name')]==player,:]) - 1
        else:
            gp = int(df.loc[idx, ('Game Info', 'Date')].split(' ')[0])
        if len(player_stats) == 0:
            new_entry = CareerStats(player_id=player_id, player_name=player, 
                                    games_played=gp,
                                    passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                                    passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                                    passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                                    passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                                    passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                                    passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                                    rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                                    rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                                    scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                                    receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                                    receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                                    receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                                    fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')])
            session.add(new_entry)
        else:
            update = session.query(CareerStats).filter_by(player_id=player_id).one()
            update.games_played+=gp
            if df.loc[idx, ('Passing', 'Att')] != 0:
                update.passing_att+=df.loc[idx, ('Passing', 'Att')]
                update.passing_cmp+=df.loc[idx, ('Passing', 'Cmp')]
                completions = update.passing_cmp
                attempts = update.passing_att
                update.passing_cmp_prc = round((completions/attempts)*100, 2)
                update.passing_yds+=df.loc[idx, ('Passing', 'Yds')]
                update.passing_tds+=df.loc[idx, ('Passing', 'TD')]
                update.passing_int+=df.loc[idx, ('Passing', 'Int')]
                # following variables are used to compute passer rating
                yards = update.passing_yds
                tds = update.passing_tds
                ints = update.passing_int
                a = ((completions/attempts) - 0.3) * 5
                b = ((yards/attempts) - 3) * 0.25
                c = (tds/attempts) * 20
                d = 2.375 - ((ints/attempts) * 25)
                rate = round(((a+b+c+d)/6) * 100, 2)
                update.passing_rate = rate
                update.passing_sacks+=df.loc[idx, ('Passing', 'Sk')]
                update.passing_sack_yds_lost+=df.loc[idx, ('Passing', 'Yds.1')]
                yds_att = round(yards/attempts,2)
                update.passing_yds_att= yds_att
                adj_yds_att = round((yards+20*tds-45*ints)/attempts, 2)
                update.passing_adj_yds_att = adj_yds_att
            if df.loc[idx, ('Rushing', 'Att')] != 0: 
                update.rushing_att+=df.loc[idx, ('Rushing', 'Att')]
                update.rushing_yds+=df.loc[idx, ('Rushing', 'Yds')]
                update.rushing_tds+=df.loc[idx, ('Rushing', 'TD')]
                yards = update.rushing_yds
                attempts = update.rushing_att
                yds_att = round(yards/attempts,2)
                update.rushing_yds_att = yds_att
            if df.loc[idx, ('Scoring', 'TD')] != 0: 
                update.scoring_tds+=df.loc[idx, ('Scoring', 'TD')]
                update.scoring_pts+=df.loc[idx, ('Scoring', 'Pts')]
            if df.loc[idx, ('Receiving', 'Rec')] != 0: 
                update.receiving_rec+=df.loc[idx, ('Receiving', 'Rec')]
                update.receiving_yds+=df.loc[idx, ('Receiving', 'Yds')]
                yards = update.receiving_yds
                receptions = update.receiving_rec
                yds_rec = round(yards/receptions, 2)
                update.receiving_yds_rec = yds_rec
                update.receiving_tds+=df.loc[idx, ('Receiving', 'TD')]
            if df.loc[idx, ('Receiving', 'Tgt')] != 0:
                update.receiving_tgts+=df.loc[idx, ('Receiving', 'Tgt')]
                receptions = update.receiving_rec
                targets = update.receiving_tgts
                catch_prc = round((receptions/targets)*100,2)
                update.receiving_catch_prc = catch_prc
                yds_tgt = round(yards/targets,2)
                update.receiving_yds_tgt = yds_tgt
            if df.loc[idx, ('Fumbles', 'Fmb')] != 0: 
                update.fumbles_fmb+=df.loc[idx, ('Fumbles', 'Fmb')]
                update.fumbles_fl+=df.loc[idx, ('Fumbles', 'FL')]

    session.commit()

def update_avg_stats(engine, session, df: pd.DataFrame, table_name: str) -> None:
    """
    Uploads the players career/season averages up to this point in their career/season into the selected table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from clean_game() 
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
            print(game_id + " + " + player_id + " combination already in database.")
            continue
        if table_name == 'career_avg_stats':
            new_entry = CareerAvgStats(game_id=game_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], 
                            player_id=player_id, team=df.loc[idx, ('Game Info', 'Tm')], 
                            passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                            passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                            passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                            passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                            passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                            passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                            rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                            rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                            scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                            receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                            receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                            receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                            fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')])
        else:
            new_entry = SeasonAvgStats(game_id=game_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], 
                            player_id=player_id, team=df.loc[idx, ('Game Info', 'Tm')], 
                            passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                            passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                            passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                            passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                            passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                            passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                            rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                            rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                            scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                            receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                            receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                            receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                            fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')])
        session.add(new_entry)
    session.commit()

def update_career_totals(engine, session, df: pd.DataFrame) -> None:
    """
    Uploads the newest game stats into the 'game_stats' table of the database.

    Args:
        engine (sqlalchemy): db connection engine
        session (sqlalchemy): db connection session
        games_df (pandas): df returned from clean_game() 

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    career_totals = pd.read_sql_query(session.query(CareerTotals).statement, engine)
    for idx in range(len(df)):
        game_id = df.loc[idx, 'game_id']
        player_id = df.loc[idx, 'player_id']
        if len(career_totals.loc[(career_totals['game_id'] == game_id) & (career_totals['player_id'] == player_id), :]) > 0:
            print(game_id + " + " + player_id + " combination already in database.")
            continue
        new_entry = CareerTotals(game_id=game_id, szn=df.loc[idx, ('Game Info', 'szn')], date=df.loc[idx, ('Game Info', 'Date')], 
                            player_id=player_id, team=df.loc[idx, ('Game Info', 'Tm')], 
                            passing_cmp=df.loc[idx, ('Passing', 'Cmp')], passing_att=df.loc[idx, ('Passing', 'Att')], 
                            passing_cmp_prc=df.loc[idx, ('Passing', 'Cmp%')], passing_yds=df.loc[idx, ('Passing', 'Yds')], 
                            passing_tds=df.loc[idx, ('Passing', 'TD')], passing_int=df.loc[idx, ('Passing', 'Int')], 
                            passing_rate=df.loc[idx, ('Passing', 'Rate')], passing_sacks=df.loc[idx, ('Passing', 'Sk')], 
                            passing_sack_yds_lost=df.loc[idx, ('Passing', 'Yds.1')], passing_yds_att=df.loc[idx, ('Passing', 'Y/A')],
                            passing_adj_yds_att=df.loc[idx, ('Passing', 'AY/A')], rushing_att=df.loc[idx, ('Rushing', 'Att')],
                            rushing_yds=df.loc[idx, ('Rushing', 'Yds')], rushing_yds_att=df.loc[idx, ('Rushing', 'Y/A')], 
                            rushing_tds=df.loc[idx, ('Rushing', 'TD')], scoring_tds=df.loc[idx, ('Scoring', 'TD')],
                            scoring_pts=df.loc[idx, ('Scoring', 'Pts')], receiving_rec=df.loc[idx, ('Receiving', 'Rec')],
                            receiving_yds=df.loc[idx, ('Receiving', 'Yds')], receiving_yds_rec=df.loc[idx, ('Receiving', 'Y/R')],
                            receiving_tds=df.loc[idx, ('Receiving', 'TD')], receiving_tgts=df.loc[idx, ('Receiving', 'Tgt')],
                            receiving_catch_prc=df.loc[idx, ('Receiving', 'Ctch%')], receiving_yds_tgt=df.loc[idx, ('Receiving', 'Y/Tgt')],
                            fumbles_fmb=df.loc[idx, ('Fumbles', 'Fmb')], fumbles_fl=df.loc[idx, ('Fumbles', 'FL')])
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
    with Session() as session:
            players = pd.read_sql("SELECT * from players", engine)
            games = pd.read_sql("SELECT * from games", engine)
            for idx in range(len(players)):
                    player_ids[players.loc[idx, 'first_name'] + ' ' + players.loc[idx, 'last_name']] = players.loc[idx, 'player_id']
            for idx in range(len(games)):
                    game_ids[str(games.loc[idx, 'date']) + games.loc[idx, 'home_team'] + games.loc[idx, 'away_team']] = games.loc[idx, 'game_id']
            with open(player_ids_path, 'wb') as dickle:
                    pickle.dump(player_ids, dickle)
            with open(game_ids_path, 'wb') as dickle:
                    pickle.dump(game_ids, dickle)
    engine.dispose()

def main() -> None:
    """
    Uploads the latest week of game_stats into the all tables of the database.

    Args:
        Nothing, claned_player_data is loaded from csv saved to data folder

    Returns:
        Nothing, the data is uploaded to the mysql database. 
    """
    df = pd.read_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/cleaned_player_data.csv")
    update_id_dicts()
    # load player and game ids
    player_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/player_ids.pkl"
    game_ids_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/game_ids.pkl"
    with open(player_ids_path, 'rb') as dickle:
        player_ids = pickle.load(dickle)
    with open(game_ids_path, 'rb') as dickle:
        game_ids = pickle.load(dickle)
    # Connect to database
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    # Create the tables / session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        update_players(engine, session, df, player_ids)
        update_games(engine, session, df, game_ids)
        with open(player_ids_path, 'rb') as dickle:
            player_ids = pickle.load(dickle)
        with open(game_ids_path, 'rb') as dickle:
            game_ids = pickle.load(dickle)
        update_game_stats(session, df, game_ids, player_ids)
        update_season_stats(engine, session, df, player_ids)
        update_career_stats(engine, session, df, player_ids)
        update_avg_stats(engine, session, df, 'career_avg_stats')
        update_avg_stats(engine, session, df, 'season_avg_stats')
        update_career_totals(engine, session, df)
    engine.dispose()