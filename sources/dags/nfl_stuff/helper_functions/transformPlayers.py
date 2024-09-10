import pandas as pd
import numpy as np
from databaseModels import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pickle
import os

def calculate_averages_per(stat1: pd.Series, stat2: pd.Series, percentage: bool) -> list:
    new_avg = []
    stat1_total = stat1.iloc[0]
    stat2_total = stat2.iloc[0]
    for i in range(1,len(stat1)):
        if stat2_total == 0:
            new_avg.append(0)
        else:
            if percentage:
                new_avg.append(round(stat1_total / stat2_total * 100,2))
            else:
                new_avg.append(round(stat1_total / stat2_total,2))
        stat1_total += stat1.iloc[i]
        stat2_total += stat2.iloc[i]
    return new_avg

def calculate_career_rate(completions: pd.Series, attempts: pd.Series, yards: pd.Series, tds: pd.Series, ints: pd.Series) -> list:
    new_avg = []
    cmp_total = completions.iloc[0]
    att_total = attempts.iloc[0]
    yds_total = yards.iloc[0]
    tds_total = tds.iloc[0]
    ints_total = ints.iloc[0]
    for i in range(1,len(completions)):
        if att_total == 0:
            new_avg.append(0)
        else:
            a = ((cmp_total/att_total) - 0.3) * 5
            b = ((yds_total/att_total) - 3) * 0.25
            c = (tds_total/att_total) * 20
            d = 2.375 - ((ints_total/att_total) * 25)
            rate = round(((a+b+c+d)/6) * 100, 2)
            new_avg.append(rate)
        cmp_total += completions.iloc[i]
        att_total += attempts.iloc[i]
        yds_total += yards.iloc[i]
        tds_total += tds.iloc[i]
        ints_total += ints.iloc[i]
    return new_avg
        
def calculate_adj_yds_att(attempts: pd.Series, yards: pd.Series, tds: pd.Series, ints: pd.Series) -> list:
    new_avg = []
    att_total = attempts.iloc[0]
    yds_total = yards.iloc[0]
    tds_total = tds.iloc[0]
    ints_total = ints.iloc[0]
    for i in range(1,len(attempts)):
        if att_total == 0:
            new_avg.append(0)
        else:
            adj_yds_att = round((yds_total+20*tds_total-45*ints_total)/att_total, 2)
            new_avg.append(adj_yds_att)
        att_total += attempts.iloc[i]
        yds_total += yards.iloc[i]
        tds_total += tds.iloc[i]
        ints_total += ints.iloc[i]
    return new_avg

def create_player_career_avgs_df(game_stats: pd.DataFrame, player_ids: dict) -> None:
    all_player_avgs = pd.DataFrame()
    for id in player_ids.values():
        df = game_stats.loc[game_stats['player_id'] == id,:]
        avgs = pd.DataFrame()
        for col in df.columns:
            if col in ['game_id', 'szn', 'date', 'player_id', 'team']:
                avgs[col] = df[col][1:]
                continue
            if col == 'passing_cmp_prc':
                avgs[col] = calculate_averages_per(stat1=df['passing_cmp'], stat2=df['passing_att'], percentage=True)
            elif col == 'passing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'rushing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['rushing_yds'], stat2=df['rushing_att'], percentage=False)
            elif col == 'receving_yds_rec':
                avgs[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'receiving_catch_prc':
                avgs[col] = calculate_averages_per(stat1=df['receiving_rec'], stat2=df['receiving_tgts'], percentage=True)
            elif col == 'receiving_yds_tgt':
                avgs[col] = calculate_averages_per(stat1=df['receiving_yds'], stat2=df['receiving_tgts'], percentage=False)
            elif col == 'passing_rate':
                avgs[col] = calculate_career_rate(df['passing_cmp'], df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col == 'passing_adj_yds_att':
                avgs[col] = calculate_adj_yds_att(df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col in ['off_snap_prc', 'off_snap_num', 'st_snap_num', 'st_snap_prc']:
                continue
                # not including snap stats in career data
            else:
                idx = 1
                total = df[col].iloc[0]
                avg_col = []
                for i in df[col][1:]:
                    new_avg = round(total / idx,2)
                    avg_col.append(new_avg)
                    total += i
                    idx += 1
                avgs[col] = avg_col
        all_player_avgs = pd.concat([all_player_avgs, avgs])
    all_player_avgs.reset_index(drop=True, inplace=True)
    all_player_avgs.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/career_avgs.csv")

def create_player_season_avgs_df(game_stats: pd.DataFrame, season: int, player_ids: dict) -> None:
    all_player_avgs = pd.DataFrame()
    for id in player_ids.values():
        df = game_stats.loc[(game_stats['player_id'] == id) & (game_stats['szn'] == season),:]
        df = df_all_years.loc[df_all_years['szn'] == year, :]
        avgs = pd.DataFrame()
        for col in df.columns:
            if col in ['game_id', 'szn', 'date', 'player_id', 'team']:
                avgs[col] = df[col][1:]
                continue
            if col == 'passing_cmp_prc':
                avgs[col] = calculate_averages_per(stat1=df['passing_cmp'], stat2=df['passing_att'], percentage=True)
            elif col == 'passing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'rushing_yds_att':
                avgs[col] = calculate_averages_per(stat1=df['rushing_yds'], stat2=df['rushing_att'], percentage=False)
            elif col == 'receving_yds_rec':
                avgs[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'receiving_catch_prc':
                avgs[col] = calculate_averages_per(stat1=df['receiving_rec'], stat2=df['receiving_tgts'], percentage=True)
            elif col == 'receiving_yds_tgt':
                avgs[col] = calculate_averages_per(stat1=df['receiving_yds'], stat2=df['receiving_tgts'], percentage=False)
            elif col == 'passing_rate':
                avgs[col] = calculate_career_rate(df['passing_cmp'], df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col == 'passing_adj_yds_att':
                avgs[col] = calculate_adj_yds_att(df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col in ['off_snap_prc', 'off_snap_num', 'st_snap_num', 'st_snap_prc']:
                continue
                # not including snap stats in career data
            else:
                idx = 1
                total = df[col].iloc[0]
                avg_col = []
                for i in df[col][1:]:
                    new_avg = round(total / idx,2)
                    avg_col.append(new_avg)
                    total += i
                    idx += 1
                avgs[col] = avg_col
            all_player_avgs = pd.concat([all_player_avgs, avgs])
    all_player_avgs.reset_index(drop=True, inplace=True)
    all_player_avgs.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/season_avgs.csv")

def create_player_career_total_df(game_stats: pd.DataFrame, player_ids: dict) -> None:
    all_player_avgs = pd.DataFrame()
    for id in player_ids.values():
        df = game_stats.loc[game_stats['player_id'] == id,:]
        totals = pd.DataFrame()
        for col in df.columns:
            if col in ['game_id', 'szn', 'date', 'player_id', 'team']:
                totals[col] = df[col][1:]
                continue
            if col == 'passing_cmp_prc':
                totals[col] = calculate_averages_per(stat1=df['passing_cmp'], stat2=df['passing_att'], percentage=True)
            elif col == 'passing_yds_att':
                totals[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'rushing_yds_att':
                totals[col] = calculate_averages_per(stat1=df['rushing_yds'], stat2=df['rushing_att'], percentage=False)
            elif col == 'receving_yds_rec':
                totals[col] = calculate_averages_per(stat1=df['passing_yds'], stat2=df['passing_att'], percentage=False)
            elif col == 'receiving_catch_prc':
                totals[col] = calculate_averages_per(stat1=df['receiving_rec'], stat2=df['receiving_tgts'], percentage=True)
            elif col == 'receiving_yds_tgt':
                totals[col] = calculate_averages_per(stat1=df['receiving_yds'], stat2=df['receiving_tgts'], percentage=False)
            elif col == 'passing_rate':
                totals[col] = calculate_career_rate(df['passing_cmp'], df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col == 'passing_adj_yds_att':
                totals[col] = calculate_adj_yds_att(df['passing_att'], df['passing_yds'],
                                                        df['passing_tds'], df['passing_int'])
            elif col in ['off_snap_prc', 'off_snap_num', 'st_snap_num', 'st_snap_prc']:
                continue
                # not including snap stats in career data
            else:
                idx = 1
                total = df[col].iloc[0]
                total_col = []
                for i in df[col][1:]:
                    new_total = total
                    total_col.append(new_total)
                    total += i
                    idx += 1
                totals[col] = total_col
        all_player_total = pd.concat([all_player_total, totals])
    all_player_total.reset_index(drop=True, inplace=True)
    all_player_total.to_csv(os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/career_totals.csv")

def main() -> None:
    season = os.environ.get("NFL_SEASON")
    # load current player ids
    curr_year_players_path = os.environ.get("AIRFLOW_HOME") + "/dags/nfl_stuff/data/curr_year_players.pkl"
    with open(curr_year_players_path, 'rb') as dickle:
        player_ids = pickle.load(dickle)
    # connect to database to load game_stats
    config_path = os.environ.get("NFL_DATABASE")
    engine = create_engine(config_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    with Session() as session:
        game_stats = pd.read_sql_query(session.query(GameStats).statement, engine)
    create_player_career_avgs_df(game_stats, player_ids)
    create_player_season_avgs_df(game_stats, season, player_ids)
    create_player_career_total_df(game_stats, player_ids)
    